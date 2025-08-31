import os
from dataclasses import dataclass
from typing import Iterable, List, Optional
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from app.models.db_models import Base, Student, FaceEmbedding, AttendanceRecord

@dataclass
class Settings:
    DATABASE_URL: str
    FACE_TOLERANCE: float = 0.6
    TEACHERS_WEBHOOK_URL: Optional[str] = None

    @staticmethod
    def from_env():
        return Settings(
            DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///./data/app.db"),
            FACE_TOLERANCE=float(os.getenv("FACE_TOLERANCE", "0.6")),
            TEACHERS_WEBHOOK_URL=os.getenv("TEACHERS_WEBHOOK_URL"),
        )

class Database:
    def __init__(self, settings: Settings):
        connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
        self.engine = create_engine(settings.DATABASE_URL, echo=False, future=True, connect_args=connect_args)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(self.engine, expire_on_commit=False, future=True)

    # --- Students
    def create_student(self, external_id: str, name: str) -> Student:
        with self.SessionLocal() as s, s.begin():
            st = Student(external_id=external_id, name=name)
            s.add(st)
            s.flush()
            return st

    def get_student(self, student_id: int) -> Optional[Student]:
        with self.SessionLocal() as s:
            return s.get(Student, student_id)

    def get_student_by_external(self, external_id: str) -> Optional[Student]:
        with self.SessionLocal() as s:
            return s.execute(select(Student).where(Student.external_id == external_id)).scalar_one_or_none()

    def list_students(self) -> List[Student]:
        with self.SessionLocal() as s:
            return list(s.execute(select(Student)).scalars())

    # --- Embeddings
    def add_embeddings(self, student_id: int, vectors: List[List[float]]) -> int:
        with self.SessionLocal() as s, s.begin():
            for v in vectors:
                s.add(FaceEmbedding(student_id=student_id, vector=[float(x) for x in v]))
            return len(vectors)

    def load_all_embeddings(self) -> List[FaceEmbedding]:
        with self.SessionLocal() as s:
            return list(s.execute(select(FaceEmbedding)).scalars())

    # --- Attendance
    def create_attendance(self, student_id: int, session_tag: str, confidence: float) -> AttendanceRecord:
        with self.SessionLocal() as s, s.begin():
            rec = AttendanceRecord(student_id=student_id, session_tag=session_tag, confidence=confidence)
            s.add(rec)
            s.flush()
            return rec

    def list_attendance_for_student(self, student_id: int) -> List[AttendanceRecord]:
        with self.SessionLocal() as s:
            return list(s.execute(select(AttendanceRecord).where(AttendanceRecord.student_id == student_id)).scalars())
