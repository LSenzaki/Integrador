from fastapi import APIRouter, UploadFile, Form
import sqlite3
import json
from app.services.face_service import get_face_encoding

router = APIRouter(prefix="/students", tags=["students"])

def get_db():
    conn = sqlite3.connect("chamada.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS pessoas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        embedding TEXT,
                        check_professor INTEGER DEFAULT 0
                    )""")
    return conn

@router.post("/cadastrar/")
async def cadastrar(nome: str = Form(...), foto: UploadFile = None):
    encoding = get_face_encoding(await foto.read())
    if not encoding:
        return {"erro": "Nenhum rosto detectado"}

    conn = get_db()
    conn.execute("INSERT INTO pessoas (nome, embedding) VALUES (?, ?)",
                 (nome, json.dumps(encoding)))
    conn.commit()
    conn.close()
    return {"mensagem": f"{nome} cadastrado com sucesso!"}
