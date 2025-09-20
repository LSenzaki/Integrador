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
from app.models.response import ResultadoReconhecimento, ResultadoSimilaridade
import json
from app.models import db_models
import numpy as np 
from typing import List

router = APIRouter(prefix="/faces", tags=["faces"])


@router.post("/reconhecer", response_model=ResultadoReconhecimento)
async def reconhecer(foto: UploadFile, db: Session = Depends(get_db)) -> ResultadoReconhecimento:
    """
    Reconhece o aluno em uma foto enviada.
    
    Parâmetros:
    - foto: UploadFile → imagem do rosto a ser reconhecido
    - db: Session → sessão do banco (injeção de dependência)

    Retorna:
    - ResultadoReconhecimento com aluno mais provável e lista de todos
    """
    encoding = get_face_encoding(foto)
    # Verifica se retornou None ou array vazio
    if encoding is None or (isinstance(encoding, np.ndarray) and encoding.size == 0):
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado na imagem enviada")

    pessoas = db.query(db_models.Pessoa).all()
    if not pessoas:
        return ResultadoReconhecimento(
            mensagem="Nenhum aluno cadastrado",
            mais_provavel=None,
            todos=[]
        )

    resultados: List[ResultadoSimilaridade] = []
    for p in pessoas:
        emb = np.array(json.loads(p.embedding))
        sim = compare_encodings(emb, encoding)
        resultados.append(ResultadoSimilaridade(
            id=p.id,
            nome=p.nome,
            similaridade=sim,
            check_professor=p.check_professor
        ))

    resultados_ordenados = sorted(resultados, key=lambda x: x.similaridade, reverse=True)
    
    return ResultadoReconhecimento(
        mais_provavel=resultados_ordenados[0]
    )
