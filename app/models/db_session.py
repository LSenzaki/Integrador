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
