from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import students, faces
from app.models import db_models
from app.models.db_session import get_db

app = FastAPI(title="Sistema de Chamada Automática")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(faces.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
