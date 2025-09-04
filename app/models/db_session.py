"""
db_session.py
-------------

Este módulo é responsável pela **configuração e gerenciamento da conexão com o banco de dados** 
utilizando SQLAlchemy. Ele cria a engine, a sessão de conexão e fornece utilitários para que 
outros módulos possam interagir com o banco de forma segura.

Responsabilidades:
- Definir a `engine` de conexão com o banco (SQLite, PostgreSQL, etc.).
- Criar a `SessionLocal`, que gera sessões independentes para cada request.
- Fornecer a função `get_db()` usada como dependência nos endpoints do FastAPI.
- Garantir abertura e fechamento corretos das conexões com o banco.

"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import db_models

DATABASE_URL = "sqlite:///./chamada.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Cria tabelas
db_models.Base.metadata.create_all(bind=engine)

# Dependência
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
