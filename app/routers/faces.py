"""
faces.py
--------
Router responsável pelo reconhecimento facial e verificação de presença.

Funcionalidades:
- Reconhecer um aluno a partir de uma foto (POST /faces/reconhecer)
- Calcula similaridade com todos os alunos cadastrados
"""

from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.face_service import get_face_encoding, compare_encodings
from app.models.db_session import get_db
import json
from app.models import db_models
import numpy as np 

router = APIRouter(prefix="/faces", tags=["faces"])

@router.post("/reconhecer")
async def reconhecer(foto: UploadFile, db: Session = Depends(get_db)):
    """
    Reconhece o aluno em uma foto enviada.
    
    Parâmetros:
    - foto: UploadFile → imagem do rosto a ser reconhecido
    - db: Session → sessão do banco (injeção de dependência)

    Retorna:
    - Mais provável aluno correspondente
    - Lista de todos os alunos com similaridade
    """
    encoding = get_face_encoding(foto)
    # Verifica se retornou None ou array vazio
    if encoding is None or (isinstance(encoding, np.ndarray) and encoding.size == 0):
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado na imagem enviada")

    pessoas = db.query(db_models.Pessoa).all()
    if not pessoas:
        return {"mensagem": "Nenhum aluno cadastrado"}

    resultados = []
    for p in pessoas:
        emb = np.array(json.loads(p.embedding))
        sim = compare_encodings(emb, encoding)
        resultados.append({"id": p.id, "nome": p.nome, "similaridade": sim, "check_professor": p.check_professor})

    resultados = sorted(resultados, key=lambda x: x["similaridade"], reverse=True)
    return {"mais_provavel": resultados[0], "todos": resultados}
