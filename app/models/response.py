# models/response.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ResultadoSimilaridade(BaseModel):
    id: int
    nome: str
    similaridade: float
    check_professor: bool

class ResultadoReconhecimento(BaseModel):
    mais_provavel: Optional[ResultadoSimilaridade] = None
   #todos: List[ResultadoSimilaridade] = Field(default_factory=list)
    mensagem: Optional[str] = None

class ErroReconhecimento(BaseModel):
    detalhe: str
    status_code: int
