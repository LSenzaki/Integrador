from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class StudentCreate(BaseModel):
    external_id: str = Field(..., max_length=64)
    name: str

class StudentOut(BaseModel):
    id: int
    external_id: str
    name: str
    class Config:
        from_attributes = True

class EnrollmentIn(BaseModel):
    student_id: int
    # para uploads multipart usamos File(...); aqui fica para API doc

class RecognizeOut(BaseModel):
    matched: bool
    student_id: Optional[int] = None
    external_id: Optional[str] = None
    name: Optional[str] = None
    confidence: Optional[float] = None  # 1 - normalized_distance
    distance: Optional[float] = None
    candidates: List[dict] = []

class AttendanceCreate(BaseModel):
    student_id: int
    session_tag: str
    confidence: float

class AttendanceOut(BaseModel):
    id: int
    student_id: int
    session_tag: str
    occurred_at: datetime
    confidence: float
    class Config:
        from_attributes = True
