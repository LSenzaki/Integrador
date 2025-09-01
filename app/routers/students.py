from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.face_service import get_face_encoding
from app.models.db_session import get_db
import json
from app.models import db_models
    

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/cadastrar")
async def cadastrar(nome: str = Form(...), foto: UploadFile = None, db: Session = Depends(get_db)):
    if not foto:
        raise HTTPException(status_code=400, detail="Imagem obrigatória")

    encoding = get_face_encoding(await foto.read())
    if not encoding:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado")

    aluno = db_models.Pessoa(nome=nome, embedding=json.dumps(encoding))
    db.add(aluno)
    db.commit()
    db.refresh(aluno)

    return {"mensagem": f"{nome} cadastrado com sucesso!", "id": aluno.id}


@router.get("/listar")
def listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(db_models.Pessoa).all()
    return
