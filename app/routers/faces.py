from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.face_service import get_face_encoding, compare_encodings
from app.models.db_session import get_db
import json
from app.models import db_models

router = APIRouter(prefix="/faces", tags=["faces"])

@router.post("/reconhecer")
async def reconhecer(foto: UploadFile, db: Session = Depends(get_db)):
    encoding = get_face_encoding(await foto.read())
    if not encoding:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado")

    pessoas = db.query(db_models.Pessoa).all()
    if not pessoas:
        return {"mensagem": "Nenhum aluno cadastrado"}

    resultados = []
    for p in pessoas:
        emb = json.loads(p.embedding)
        sim = compare_encodings(emb, encoding)
        resultados.append({"id": p.id, "nome": p.nome, "similaridade": sim, "check_professor": p.check_professor})

    resultados = sorted(resultados, key=lambda x: x["similaridade"], reverse=True)
    return {"mais_provavel": resultados[0], "todos": resultados}
