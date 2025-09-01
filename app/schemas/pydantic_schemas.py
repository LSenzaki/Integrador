from pydantic import BaseModel

class PessoaCreate(BaseModel):
    nome: str

class PessoaOut(BaseModel):
    id: int
    nome: str
    check_professor: bool
