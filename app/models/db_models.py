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

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    embedding = Column(String, nullable=False)  # JSON string
    check_professor = Column(Boolean, default=False)
