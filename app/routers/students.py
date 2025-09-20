"""
students.py
------------
Router responsável pelo gerenciamento de alunos.

Funcionalidades:
- Cadastro de alunos com foto (POST /students/cadastrar)
- Listagem de alunos cadastrados (GET /students/listar)
"""

from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.face_service import get_face_encoding
from app.models.db_session import get_db
from app.models.response import ResultadoReconhecimento, ResultadoSimilaridade
import json
from app.models import db_models


router = APIRouter(prefix="/students", tags=["students"])

@router.post("/cadastrar")
async def cadastrar(nome: str = Form(...), foto: UploadFile = None,
                    db: Session = Depends(get_db)):
    """
    Cadastra um aluno no banco de dados.
    
    Parâmetros:
    - nome: str → nome do aluno
    - foto: UploadFile → imagem do rosto do aluno
    - db: Session → sessão do banco (injeção de dependência)

    Retorna:
    - Mensagem de sucesso e ID do aluno cadastrado
    """     
    if not foto:
        raise HTTPException(status_code=400, detail="Imagem obrigatória")

    encoding = get_face_encoding(foto)
    if encoding is None:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado")

    aluno = db_models.Pessoa(
        nome=nome,
        embedding=json.dumps(encoding.tolist())  # <- aqui o ajuste
    )
    db.add(aluno)
    db.commit()
    db.refresh(aluno)

    return {"mensagem": f"{nome} cadastrado com sucesso!", "id": aluno.id}


@router.get("/listar")
def listar_alunos(db: Session = Depends(get_db)):
    """
    Retorna a lista de todos os alunos cadastrados.
    """
    alunos = db.query(db_models.Pessoa).all()
    return [
        {
            "id": aluno.id,
            "nome": aluno.nome,
            "check_professor": aluno.check_professor
        }
        for aluno in alunos
    ]

@router.delete("/remover/{aluno_id}")
def remover_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """
    Remove um aluno do banco pelo ID.
    """
    aluno = db.query(db_models.Pessoa).filter(db_models.Pessoa.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    db.delete(aluno)
    db.commit()
    return {"mensagem": f"Aluno '{aluno.nome}' removido com sucesso"}