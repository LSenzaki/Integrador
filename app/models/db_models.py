from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, JSON, func, UniqueConstraint, Index

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)  # ID do sistema dos professores
    name: Mapped[str] = mapped_column(String(255), index=True)
    encodings = relationship("FaceEmbedding", back_populates="student", cascade="all, delete-orphan")
    attendances = relationship("AttendanceRecord", back_populates="student", cascade="all, delete-orphan")

class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    # 128 floats; armazenamos como JSON para portabilidade (poderia ser ARRAY/BLOB)
    vector: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    student = relationship("Student", back_populates="encodings")

    __table_args__ = (
        Index("ix_face_embeddings_student", "student_id"),
    )

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    occurred_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    source: Mapped[str] = mapped_column(String(32), default="face")  # face|manual|import
    session_tag: Mapped[str] = mapped_column(String(64), index=True) # ex: Aula-2025-08-31-Quimica-A
    confidence: Mapped[Float] = mapped_column(Float)

    student = relationship("Student", back_populates="attendances")

    __table_args__ = (
        UniqueConstraint("student_id", "session_tag", name="uq_attendance_student_session"),
    )
