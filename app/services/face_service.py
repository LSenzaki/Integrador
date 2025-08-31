import io
import numpy as np
import face_recognition
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import httpx

from app.services.db_service import Database, Settings
from app.models.db_models import FaceEmbedding, Student

@dataclass
class Candidate:
    student_id: int
    external_id: str
    name: str
    distance: float
    confidence: float  # mapeada de distância

def distance_to_confidence(d: float, tol: float) -> float:
    # mapeamento simples: 1.0 na distância 0; 0.0 em d>=tol
    return max(0.0, 1.0 - (d / tol))

class FaceService:
    def __init__(self, db: Database, tolerance: float = 0.6, webhook_url: Optional[str] = None):
        self.db = db
        self.tolerance = tolerance
        self.webhook_url = webhook_url
        self._cache_vectors: np.ndarray = None  # shape (N,128)
        self._cache_meta: List[Tuple[int, str, str]] = []  # (student_id, external_id, name)
        self._load_cache()

    def _load_cache(self):
        rows: List[FaceEmbedding] = self.db.load_all_embeddings()
        if not rows:
            self._cache_vectors = np.empty((0,128), dtype=np.float32)
            self._cache_meta = []
            return
        vecs, meta = [], []
        for r in rows:
            v = np.array(r.vector, dtype=np.float32)
            if v.shape[0] == 128:
                vecs.append(v)
                # fetch student lazily? Keep in memory to evitar join grande
                # Otimização: poderia fazer JOIN no load_all_embeddings
                # Aqui resolvemos pegando por relacionamento
                st: Student = r.student
                meta.append((st.id, st.external_id, st.name))
        self._cache_vectors = np.stack(vecs, axis=0) if vecs else np.empty((0,128), dtype=np.float32)
        self._cache_meta = meta

    # Chamar ao inscrever novos encodings
    def refresh_cache(self):
        self._load_cache()

    # --- Enroll
    def enroll_from_image_bytes(self, student_id: int, content: bytes) -> int:
        img = face_recognition.load_image_file(io.BytesIO(content))
        boxes = face_recognition.face_locations(img, model="hog")  # 'cnn' se GPU disponível
        encs = face_recognition.face_encodings(img, boxes)
        if not encs:
            return 0
        n = self.db.add_embeddings(student_id, [e.tolist() for e in encs])
        self.refresh_cache()
        return n

    # --- Recognize
    def recognize_from_image_bytes(self, content: bytes, top_k: int = 3) -> Dict:
        img = face_recognition.load_image_file(io.BytesIO(content))
        boxes = face_recognition.face_locations(img, model="hog")
        encs = face_recognition.face_encodings(img, boxes)
        if not encs:
            return {"faces": []}

        faces_out = []
        for enc in encs:
            if self._cache_vectors.shape[0] == 0:
                faces_out.append({"matched": False, "candidates": []})
                continue

            # Distâncias para todos
            diffs = self._cache_vectors - enc.astype(np.float32)
            dists = np.sqrt(np.sum(diffs * diffs, axis=1))
            # Ordena
            idx = np.argsort(dists)[:top_k]
            cand_list: List[Candidate] = []
            for i in idx:
                d = float(dists[i])
                sid, ext, name = self._cache_meta[i]
                cand_list.append(Candidate(
                    student_id=sid, external_id=ext, name=name,
                    distance=d, confidence=distance_to_confidence(d, self.tolerance)
                ))
            # melhor candidato
            best = cand_list[0]
            matched = best.distance <= self.tolerance
            faces_out.append({
                "matched": matched,
                "student_id": best.student_id if matched else None,
                "external_id": best.external_id if matched else None,
                "name": best.name if matched else None,
                "distance": best.distance,
                "confidence": best.confidence,
                "candidates": [c.__dict__ for c in cand_list],
            })
        return {"faces": faces_out}

    # --- Attendance + webhook opcional
    async def create_attendance_and_notify(self, student_id: int, session_tag: str, confidence: float):
        rec = self.db.create_attendance(student_id, session_tag, confidence)
        if self.webhook_url:
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    await client.post(self.webhook_url, json={
                        "student_id": student_id,
                        "session_tag": session_tag,
                        "confidence": confidence,
                        "occurred_at": rec.occurred_at.isoformat(),
                    })
            except Exception:
                # logar em prod; aqui silencioso
                pass
        return rec
