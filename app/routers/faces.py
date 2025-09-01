from fastapi import APIRouter, UploadFile
import sqlite3
import json
from app.services.face_service import get_face_encoding, compare_encodings

router = APIRouter(prefix="/faces", tags=["faces"])

def get_db():
    conn = sqlite3.connect("chamada.db")
    return conn

@router.post("/reconhecer/")
async def reconhecer(foto: UploadFile):
    encoding = get_face_encoding(await foto.read())
    if not encoding:
        return {"erro": "Nenhum rosto detectado"}

    conn = get_db()
    cursor = conn.execute("SELECT id, nome, embedding FROM pessoas")
    pessoas = cursor.fetchall()
    conn.close()

    resultados = []
    for pid, nome, emb_str in pessoas:
        emb = json.loads(emb_str)
        sim = compare_encodings(emb, encoding)
        resultados.append({"id": pid, "nome": nome, "similaridade": sim})

    if resultados:
        resultados = sorted(resultados, key=lambda x: x["similaridade"], reverse=True)
        return {"mais_provavel": resultados[0], "todos": resultados}
    else:
        return {"mensagem": "Nenhum usuário cadastrado"}
