from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router

app.include_router(auth_router)

# Para rodar, executar no terminarl -> uvicorn main:app --reload