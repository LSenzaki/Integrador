"""
db_models.py
------------

Este módulo contém as definições das entidades do banco de dados. 
Cada classe mapeia uma tabela no banco de dados relacional.

Resposável por:
- Definir tabelas e colunas que representam os dados persistidos.
- Especificar relacionamentos (ex.: One-to-Many, Many-to-Many).
- Definir chaves primárias, estrangeiras e restrições.
- Garantir a integridade dos dados no nível do ORM.

"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.db_session import Base  # só importa, não circular

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    embedding = Column(String)  # JSON com vetor do rosto
    check_professor = Column(Boolean, default=False)

    chamadas = relationship("Chamada", back_populates="pessoa")


class Chamada(Base):
    __tablename__ = "chamadas"

    id = Column(Integer, primary_key=True, index=True)
    pessoa_id = Column(Integer, ForeignKey("pessoas.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    origem = Column(String, default="upload")

    pessoa = relationship("Pessoa", back_populates="chamadas")

