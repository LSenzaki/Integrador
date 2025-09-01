from fastapi import FastAPI
from app.routers import students, faces

app = FastAPI(title="Teste Chamada Local")

app.include_router(students.router)
app.include_router(faces.router)
