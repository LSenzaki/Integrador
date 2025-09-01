"""
webcam.py
---------
Router para teste de reconhecimento facial em tempo real usando webcam local.
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import cv2
from app.services.face_service import get_face_encoding, compare_encodings
from app.models.db_session import SessionLocal
from app.models import db_models
import json

router = APIRouter(prefix="/webcam", tags=["webcam"])

@router.get("/reconhecer")
def reconhecer_webcam():
    """
    Captura um frame da webcam, realiza reconhecimento facial e retorna resultados JSON.
    """
    # Conecta ao banco
    db = SessionLocal()
    pessoas = db.query(db_models.Pessoa).all()
    db.close()

    if not pessoas:
        return JSONResponse(content={"mensagem": "Nenhum aluno cadastrado"}, status_code=404)

    embeddings_db = [(p.id, p.nome, json.loads(p.embedding)) for p in pessoas]

    # Captura um frame da webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return JSONResponse(content={"erro": "Não foi possível acessar a webcam"}, status_code=500)

    # Reduz resolução para acelerar
    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    # Extrai embedding
    encodings = get_face_encoding(cv2.imencode('.jpg', small_frame)[1].tobytes())
    if not encodings:
        return JSONResponse(content={"mensagem": "Nenhum rosto detectado"}, status_code=404)

    resultados = []
    for pid, nome, emb in embeddings_db:
        sim = compare_encodings(emb, encodings)
        resultados.append({"id": pid, "nome": nome, "similaridade": sim})

    resultados = sorted(resultados, key=lambda x: x["similaridade"], reverse=True)
    return {"mais_provavel": resultados[0], "todos": resultados}
