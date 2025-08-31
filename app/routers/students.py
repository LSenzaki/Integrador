from fastapi import APIRouter, Depends
from app.schemas.pydantic_schemas import StudentCreate, StudentOut, AttendanceOut
from app.services.db_service import Database
from fastapi import Request

router = APIRouter()

def get_db(req: Request) -> Database:
    return req.app.state.db

@router.post("", response_model=StudentOut)
def create_student(payload: StudentCreate, db: Database = Depends(get_db)):
    st = db.create_student(external_id=payload.external_id, name=payload.name)
    return st

@router.get("", response_model=list[StudentOut])
def list_students(db: Database = Depends(get_db)):
    return db.list_students()

@router.get("/{student_id}/attendance", response_model=list[AttendanceOut])
def list_attendance(student_id: int, db: Database = Depends(get_db)):
    return db.list_attendance_for_student(student_id)
