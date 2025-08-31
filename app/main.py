from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import faces, students
from app.services.face_service import FaceService
from app.services.db_service import Database, Settings

app = FastAPI(title="Attendance via Face Recognition", version="0.1.0")

# CORS (ajuste para domínios do sistema dos professores)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializações globais
settings = Settings.from_env()
db = Database(settings)
face_service = FaceService(db=db, tolerance=settings.FACE_TOLERANCE)

# Injeção via state
app.state.db = db
app.state.face_service = face_service

# Routers
app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(faces.router, prefix="/faces", tags=["faces"])

@app.get("/health")
def health():
    return {"status": "ok"}
