from fastapi import APIRouter, UploadFile, File, Form, Depends, Request, HTTPException
from app.schemas.pydantic_schemas import RecognizeOut, AttendanceOut
from app.services.db_service import Database
from app.services.face_service import FaceService
from typing import Optional

router = APIRouter()

def get_db(req: Request) -> Database:
    return req.app.state.db

def get_face_service(req: Request) -> FaceService:
    return req.app.state.face_service

@router.post("/enroll")
async def enroll_face(
    student_id: int = Form(...),
    image: UploadFile = File(...),
    db: Database = Depends(get_db),
    face_service: FaceService = Depends(get_face_service),
):
    if not db.get_student(student_id):
        raise HTTPException(404, "student not found")
    content = await image.read()
    n = face_service.enroll_from_image_bytes(student_id, content)
    if n == 0:
        raise HTTPException(422, "no face detected")
    return {"embeddings_added": n}

@router.post("/recognize", response_model=dict)
async def recognize(
    image: UploadFile = File(...),
    session_tag: Optional[str] = Form(None),  # se presente, já registra presença
    face_service: FaceService = Depends(get_face_service),
):
    content = await image.read()
    result = face_service.recognize_from_image_bytes(content)
    out_faces = []
    for face in result["faces"]:
        if session_tag and face.get("matched"):
            rec = await face_service.create_attendance_and_notify(
                student_id=face["student_id"],
                session_tag=session_tag,
                confidence=face["confidence"] or 0.0
            )
            face["attendance_record_id"] = rec.id
        out_faces.append(face)
    return {"faces": out_faces}
