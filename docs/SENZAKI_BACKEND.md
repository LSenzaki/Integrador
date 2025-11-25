# 🚀 GUIA DE ESTUDO - BACKEND (Senzaki)

## 📋 Índice
1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Banco de Dados](#banco-de-dados)
5. [Modelos SQLAlchemy](#modelos-sqlalchemy)
6. [API FastAPI](#api-fastapi)
7. [Serviços de Reconhecimento Facial](#serviços-de-reconhecimento-facial)
8. [Configurações e Variáveis de Ambiente](#configurações-e-variáveis-de-ambiente)
9. [Rotas da API](#rotas-da-api)
10. [Fluxo de Cadastro e Reconhecimento](#fluxo-de-cadastro-e-reconhecimento)

---

## 🎯 Visão Geral da Arquitetura

O backend foi desenvolvido usando **arquitetura em camadas** (layered architecture), separando responsabilidades:

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │  ← Routers (endpoints HTTP)
├─────────────────────────────────────┤
│       Service Layer (Lógica)        │  ← Services (reconhecimento, DB)
├─────────────────────────────────────┤
│      Data Layer (Modelos ORM)       │  ← SQLAlchemy Models
├─────────────────────────────────────┤
│     Database (Supabase/PostgreSQL)  │  ← Armazenamento persistente
└─────────────────────────────────────┘
```

### Princípios Aplicados:
- **Separation of Concerns**: Cada camada tem responsabilidade única
- **Dependency Injection**: FastAPI injeta dependências automaticamente
- **RESTful API**: Endpoints seguem padrões REST
- **Type Safety**: Pydantic schemas garantem validação de dados

---

## 🛠️ Tecnologias Utilizadas

### 1. **FastAPI**
Framework web moderno, rápido e com documentação automática.

**Por que FastAPI?**
- ✅ **Performance**: Baseado em Starlette e Pydantic (async/await)
- ✅ **Type Hints**: Validação automática com Python type hints
- ✅ **Documentação**: Swagger UI automático em `/docs`
- ✅ **Async Support**: Perfeito para operações I/O intensivas

**Exemplo de uso:**
```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
```

### 2. **SQLAlchemy**
ORM (Object-Relational Mapping) para Python.

**Conceito de ORM:**
Transforma tabelas do banco em classes Python:
```python
# Tabela SQL
CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255)
);

# Vira classe Python
class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
```

### 3. **Supabase (PostgreSQL)**
Backend-as-a-Service com PostgreSQL gerenciado.

**Vantagens:**
- ✅ PostgreSQL com features enterprise
- ✅ API REST automática
- ✅ Autenticação e autorização integradas
- ✅ Storage para arquivos

### 4. **Face Recognition Libraries**
- **face_recognition**: Biblioteca rápida baseada em dlib
- **DeepFace**: Framework com múltiplos modelos de deep learning

---

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py              # Inicialização do pacote
│   ├── main.py                  # Aplicação FastAPI principal
│   ├── config.py                # Configurações e variáveis de ambiente
│   │
│   ├── models/                  # Camada de Dados (ORM)
│   │   ├── db_models.py         # Modelos SQLAlchemy
│   │   ├── db_session.py        # Configuração do banco
│   │   └── response.py          # Modelos de resposta
│   │
│   ├── routers/                 # Camada de API (Endpoints)
│   │   ├── alunos.py            # Endpoints de alunos
│   │   ├── turmas.py            # Endpoints de turmas
│   │   ├── professores.py       # Endpoints de professores
│   │   └── presencas.py         # Endpoints de presenças
│   │
│   ├── services/                # Camada de Lógica de Negócio
│   │   ├── db_service.py        # Serviço de banco de dados
│   │   ├── face_service.py      # Reconhecimento com face_recognition
│   │   ├── deepface_service.py  # Reconhecimento com DeepFace
│   │   ├── hybrid_face_service.py # Sistema híbrido
│   │   └── comparison_service.py  # Comparação de modelos
│   │
│   └── schemas/                 # Schemas Pydantic (Validação)
│       └── pydantic_schemas.py  # Modelos de entrada/saída
│
├── scripts/                     # Scripts utilitários
├── tests/                       # Testes automatizados
├── database_schema.sql          # Schema do banco de dados
└── requirements.txt             # Dependências Python
```

---

## 🗄️ Banco de Dados

### Schema Completo

O banco foi projetado para suportar um sistema de presença com reconhecimento facial:

```sql
-- TABELA: turmas (Classes)
CREATE TABLE turmas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABELA: professores
CREATE TABLE professores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABELA: turmas_professores (Many-to-Many)
CREATE TABLE turmas_professores (
    id SERIAL PRIMARY KEY,
    turma_id INTEGER REFERENCES turmas(id) ON DELETE CASCADE,
    professor_id INTEGER REFERENCES professores(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(turma_id, professor_id)
);

-- TABELA: alunos
CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    turma_id INTEGER REFERENCES turmas(id),
    check_professor BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABELA: face_embeddings (Vetores faciais)
CREATE TABLE face_embeddings (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER REFERENCES alunos(id) ON DELETE CASCADE,
    embedding BYTEA NOT NULL,  -- Vetor serializado (pickle)
    foto_nome VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABELA: presencas
CREATE TABLE presencas (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER REFERENCES alunos(id),
    turma_id INTEGER REFERENCES turmas(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confianca FLOAT,
    validado BOOLEAN DEFAULT FALSE,
    validado_por INTEGER REFERENCES professores(id),
    validado_em TIMESTAMP
);
```

### Relacionamentos:

```
turmas ←→ turmas_professores ←→ professores
  ↓                                    ↓
alunos                           (valida)
  ↓                                    ↓
face_embeddings              presencas
```

### Índices para Performance:
```sql
-- Buscas por nome de turma
CREATE INDEX idx_turmas_nome ON turmas(nome);

-- Busca de alunos por turma
CREATE INDEX idx_alunos_turma ON alunos(turma_id);

-- Busca de embeddings por aluno
CREATE INDEX idx_face_embeddings_aluno ON face_embeddings(aluno_id);

-- Filtros de presença
CREATE INDEX idx_presencas_turma_timestamp ON presencas(turma_id, timestamp);
```

---

## 🧩 Modelos SQLAlchemy

### 1. Modelo Turma

```python
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.db_session import Base

class Turma(Base):
    __tablename__ = "turmas"
    
    # Colunas
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), 
                       default=datetime.utcnow, 
                       onupdate=datetime.utcnow)
    
    # Relacionamentos (ORM Magic!)
    alunos = relationship("Aluno", back_populates="turma")
    presencas = relationship("Presenca", back_populates="turma")
    professores = relationship(
        "Professor",
        secondary="turmas_professores",  # Tabela intermediária
        back_populates="turmas"
    )
```

**Conceitos SQLAlchemy:**

- **`Column`**: Define colunas da tabela
- **`relationship`**: Define relações entre tabelas (JOINs automáticos)
- **`back_populates`**: Bidirecionalidade (Turma ↔ Aluno)
- **`secondary`**: Para relações many-to-many

### 2. Modelo Aluno

```python
class Aluno(Base):
    __tablename__ = "alunos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"))
    check_professor = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), 
                       default=datetime.utcnow, 
                       onupdate=datetime.utcnow)
    
    # Relacionamentos
    turma = relationship("Turma", back_populates="alunos")
    embeddings = relationship("FaceEmbedding", back_populates="aluno", 
                             cascade="all, delete-orphan")
    presencas = relationship("Presenca", back_populates="aluno")
```

**`cascade="all, delete-orphan"`**: Quando deletar aluno, deleta embeddings automaticamente.

### 3. Modelo FaceEmbedding

```python
class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"))
    embedding = Column(LargeBinary, nullable=False)  # Vetor facial serializado
    foto_nome = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    
    # Relacionamento
    aluno = relationship("Aluno", back_populates="embeddings")
```

**Armazenamento de Embeddings:**
```python
import pickle

# Salvar vetor no banco
vetor_facial = [0.1, 0.2, 0.3, ...]  # Array NumPy 128D ou 512D
embedding_bytes = pickle.dumps(vetor_facial)

# Recuperar do banco
vetor_recuperado = pickle.loads(embedding_bytes)
```

---

## 🌐 API FastAPI

### Estrutura main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import turmas, professores, alunos, presencas

app = FastAPI(title="Sistema de Chamada Automática")

# CORS - Permite requisições do frontend
origins = [
    "http://localhost:3000",  # React local
    "https://seu-frontend.com",
    "*"  # Para desenvolvimento (inseguro em produção!)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)

# Registrar routers
app.include_router(turmas.router)
app.include_router(professores.router)
app.include_router(alunos.router)
app.include_router(presencas.router)

@app.get("/")
def root():
    return {
        "message": "Sistema de Chamada Automática API",
        "version": "3.0",
        "endpoints": {
            "docs": "/docs",
            "turmas": "/turmas",
            "alunos": "/alunos",
            "presencas": "/presencas"
        }
    }
```

### Dependency Injection

FastAPI usa **Depends()** para injetar dependências:

```python
from fastapi import Depends
from app.services.db_service import get_db_manager, SupabaseDB

@router.get("/alunos")
def list_alunos(db: SupabaseDB = Depends(get_db_manager)):
    # db é injetado automaticamente!
    return db.list_alunos()
```

**Como funciona:**
1. FastAPI chama `get_db_manager()`
2. Retorna instância de `SupabaseDB`
3. Injeta no parâmetro `db`
4. Disponível na função

---

## 🔍 Serviços de Reconhecimento Facial

### 1. Face Service (face_recognition)

```python
# app/services/face_service.py
import face_recognition
import numpy as np
from fastapi import UploadFile
from PIL import Image
import io

def get_face_encoding(file: UploadFile) -> np.ndarray:
    """
    Extrai embedding facial de uma imagem.
    
    Returns:
        Array NumPy 128D representando o rosto
    """
    # Ler arquivo
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # Converter para RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Converter para array NumPy
    image_array = np.array(image)
    
    # Detectar rostos e gerar encoding
    face_locations = face_recognition.face_locations(image_array)
    
    if not face_locations:
        return None
    
    # Gerar embedding (128 dimensões)
    encodings = face_recognition.face_encodings(image_array, face_locations)
    
    return encodings[0] if encodings else None


def recognize_face(
    face_encoding: np.ndarray,
    known_faces: List[Dict]
) -> Tuple[int, float]:
    """
    Compara encoding com rostos conhecidos.
    
    Args:
        face_encoding: Vetor 128D do rosto a reconhecer
        known_faces: Lista de dicts com 'id' e 'embedding'
    
    Returns:
        (aluno_id, confianca) ou (None, 0.0)
    """
    if not known_faces:
        return None, 0.0
    
    # Extrair embeddings conhecidos
    known_encodings = [f['embedding'] for f in known_faces]
    
    # Calcular distâncias euclidianas
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    
    # Encontrar melhor match
    min_distance = np.min(distances)
    best_match_idx = np.argmin(distances)
    
    # Converter distância para confiança (0-100%)
    confidence = (1.0 - min_distance) * 100
    
    # Threshold: aceitar se distância < 0.6 (confiança > 40%)
    if min_distance < 0.6:
        return known_faces[best_match_idx]['id'], confidence
    
    return None, 0.0
```

**Técnica: Distância Euclidiana**
```
distance = √(Σ(a[i] - b[i])²)

Quanto menor a distância, mais similar os rostos.
```

### 2. DeepFace Service

```python
# app/services/deepface_service.py
from deepface import DeepFace
import numpy as np

def get_deepface_encoding(
    file: UploadFile,
    model_name: str = "Facenet512"
) -> np.ndarray:
    """
    Extrai embedding usando DeepFace.
    
    Models disponíveis:
    - Facenet512: 512D (mais preciso)
    - Facenet: 128D
    - VGG-Face: 2622D
    - ArcFace: 512D
    """
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image_array = np.array(image)
    
    # DeepFace.represent retorna lista de embeddings
    embeddings = DeepFace.represent(
        img_path=image_array,
        model_name=model_name,
        enforce_detection=True,
        detector_backend="opencv"
    )
    
    return np.array(embeddings[0]["embedding"])


def recognize_face_deepface(
    face_encoding: np.ndarray,
    known_faces: List[Dict],
    metric: str = "cosine"
) -> Tuple[int, float, float]:
    """
    Reconhece rosto usando DeepFace.
    
    Métricas:
    - cosine: Similaridade de cosseno
    - euclidean: Distância euclidiana
    - euclidean_l2: Distância euclidiana normalizada
    """
    if not known_faces:
        return None, 0.0, 1.0
    
    best_match = None
    best_confidence = 0.0
    best_distance = float('inf')
    
    for known_face in known_faces:
        known_encoding = known_face['embedding']
        
        # Calcular distância
        if metric == "cosine":
            # Similaridade de cosseno: [-1, 1]
            similarity = np.dot(face_encoding, known_encoding) / (
                np.linalg.norm(face_encoding) * np.linalg.norm(known_encoding)
            )
            distance = 1 - similarity
            confidence = similarity * 100
        else:
            # Distância euclidiana
            distance = np.linalg.norm(face_encoding - known_encoding)
            confidence = (1.0 - min(distance, 1.0)) * 100
        
        if distance < best_distance:
            best_distance = distance
            best_confidence = confidence
            best_match = known_face['id']
    
    # Threshold DeepFace (mais rigoroso)
    threshold = 0.4 if metric == "cosine" else 1.0
    
    if best_distance < threshold:
        return best_match, best_confidence, best_distance
    
    return None, 0.0, best_distance
```

### 3. Sistema Híbrido

Combina ambos modelos para melhor performance:

```python
# app/services/hybrid_face_service.py

HIGH_CONFIDENCE_THRESHOLD = 55.0  # face_recognition confiável
LOW_CONFIDENCE_THRESHOLD = 35.0   # face_recognition duvidoso

def recognize_face_hybrid(
    file: UploadFile,
    known_faces: List[Dict],
    mode: str = "smart"
) -> dict:
    """
    Estratégia SMART:
    1. Tenta face_recognition (rápido ~0.09s)
    2. Se confiança >= 55%: aceita
    3. Se confiança 35-55%: valida com DeepFace
    4. Se confiança < 35%: usa DeepFace como autoridade
    """
    start_time = time.time()
    
    # PASSO 1: face_recognition
    fr_encoding = get_face_encoding(file)
    fr_result = recognize_face(fr_encoding, known_faces)
    
    if fr_result:
        fr_id, fr_confidence = fr_result
        
        # Alta confiança: aceita direto
        if fr_confidence >= HIGH_CONFIDENCE_THRESHOLD:
            return {
                "aluno_id": fr_id,
                "confidence": fr_confidence,
                "method": "face_recognition_only",
                "time": time.time() - start_time
            }
        
        # Confiança média: validar com DeepFace
        elif fr_confidence >= LOW_CONFIDENCE_THRESHOLD:
            df_encoding = get_deepface_encoding(file)
            df_result = recognize_face_deepface(df_encoding, known_faces)
            
            if df_result:
                df_id, df_confidence, df_distance = df_result
                
                # Concordam?
                if df_id == fr_id:
                    return {
                        "aluno_id": fr_id,
                        "confidence": (fr_confidence * 0.6 + df_confidence * 0.4),
                        "method": "hybrid_validated",
                        "agreement": True,
                        "time": time.time() - start_time
                    }
    
    # FALLBACK: Apenas DeepFace
    df_encoding = get_deepface_encoding(file)
    df_result = recognize_face_deepface(df_encoding, known_faces)
    
    if df_result:
        df_id, df_confidence, _ = df_result
        return {
            "aluno_id": df_id,
            "confidence": df_confidence,
            "method": "deepface_fallback",
            "time": time.time() - start_time
        }
    
    return {
        "aluno_id": None,
        "confidence": 0.0,
        "method": "no_match",
        "time": time.time() - start_time
    }
```

---

## ⚙️ Configurações e Variáveis de Ambiente

### config.py

```python
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carregar .env
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Aplicação
    APP_NAME: str = "Chamada Facial API"
    APP_VERSION: str = "1.0.0"
    SIMILARITY_THRESHOLD: float = 0.6
    
    class Config:
        case_sensitive = True
        env_file_encoding = 'utf-8'

settings = Settings()
```

### Arquivo .env

```bash
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-secreta-aqui

# Aplicação
SIMILARITY_THRESHOLD=0.6
```

**Segurança:** Nunca commitar .env no Git! Adicionar ao `.gitignore`:
```
.env
__pycache__/
*.pyc
```

---

## 🛣️ Rotas da API

### 1. Alunos (`/alunos`)

```python
# app/routers/alunos.py
from fastapi import APIRouter, Depends, UploadFile, File, Form

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get("/")
def list_alunos(
    turma_id: Optional[int] = None,
    db: SupabaseDB = Depends(get_db_manager)
):
    """Lista todos os alunos, opcionalmente filtrados por turma."""
    return db.list_alunos(turma_id=turma_id)


@router.post("/cadastrar")
async def cadastrar_aluno(
    nome: str = Form(...),
    turma_id: int = Form(...),
    fotos: List[UploadFile] = File(...),
    db: SupabaseDB = Depends(get_db_manager)
):
    """
    Cadastra aluno com múltiplas fotos.
    
    Processo:
    1. Cria registro do aluno
    2. Para cada foto:
       - Extrai embedding facial
       - Salva na tabela face_embeddings
    """
    # Criar aluno
    aluno = db.create_aluno(nome=nome, turma_id=turma_id)
    
    embeddings_salvos = 0
    
    for foto in fotos:
        # Extrair embedding
        encoding = get_face_encoding(foto)
        
        if encoding is not None:
            # Salvar no banco
            db.save_face_embedding(
                aluno_id=aluno['id'],
                embedding=encoding,
                foto_nome=foto.filename
            )
            embeddings_salvos += 1
    
    return {
        "status": "success",
        "aluno": aluno,
        "embeddings_salvos": embeddings_salvos
    }


@router.post("/reconhecer")
async def reconhecer_aluno(
    foto: UploadFile = File(...),
    turma_id: int = Form(...),
    mode: str = Form("smart"),
    db: SupabaseDB = Depends(get_db_manager)
):
    """
    Reconhece aluno e registra presença.
    
    Args:
        foto: Foto do aluno
        turma_id: ID da turma
        mode: Modo do sistema híbrido
    """
    # Buscar embeddings da turma
    known_faces = db.get_turma_embeddings(turma_id)
    
    # Reconhecer usando sistema híbrido
    result = recognize_face_hybrid(foto, known_faces, mode)
    
    if result['aluno_id']:
        # Registrar presença
        presenca = db.registrar_presenca(
            aluno_id=result['aluno_id'],
            turma_id=turma_id,
            confianca=result['confidence']
        )
        
        return {
            "status": "success",
            "message": f"Presença registrada!",
            "aluno_id": result['aluno_id'],
            "confidence": result['confidence'],
            "method": result['method'],
            "presenca_id": presenca['id']
        }
    
    return {
        "status": "not_found",
        "message": "Aluno não reconhecido"
    }
```

### 2. Turmas (`/turmas`)

```python
@router.get("/turmas")
def list_turmas(db: SupabaseDB = Depends(get_db_manager)):
    """Lista todas as turmas."""
    return db.list_turmas()


@router.post("/turmas")
def create_turma(
    nome: str,
    db: SupabaseDB = Depends(get_db_manager)
):
    """Cria nova turma."""
    return db.create_turma(nome=nome)


@router.get("/turmas/{turma_id}/alunos")
def get_turma_alunos(
    turma_id: int,
    db: SupabaseDB = Depends(get_db_manager)
):
    """Lista alunos de uma turma específica."""
    return db.list_alunos(turma_id=turma_id)
```

### 3. Presenças (`/presencas`)

```python
@router.get("/presencas")
def list_presencas(
    turma_id: Optional[int] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    db: SupabaseDB = Depends(get_db_manager)
):
    """
    Lista presenças com filtros.
    
    Filtros:
    - turma_id: Filtrar por turma
    - data_inicio/data_fim: Intervalo de datas
    """
    return db.list_presencas(
        turma_id=turma_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


@router.put("/presencas/{presenca_id}/validar")
def validar_presenca(
    presenca_id: int,
    professor_id: int,
    db: SupabaseDB = Depends(get_db_manager)
):
    """Professor valida uma presença."""
    return db.validar_presenca(presenca_id, professor_id)
```

---

## 🔄 Fluxo de Cadastro e Reconhecimento

### Fluxo 1: Cadastro de Aluno

```
┌─────────────┐
│  Frontend   │
└──────┬──────┘
       │ POST /alunos/cadastrar
       │ {nome, turma_id, fotos[]}
       ▼
┌─────────────────┐
│  alunos.py      │  ← Router
└────────┬────────┘
         │ create_aluno()
         ▼
┌─────────────────┐
│  db_service.py  │  ← Cria aluno no banco
└────────┬────────┘
         │
         │ Para cada foto:
         ▼
┌─────────────────┐
│ face_service.py │  ← Extrai embedding
└────────┬────────┘
         │ get_face_encoding()
         │ retorna array 128D
         ▼
┌─────────────────┐
│  db_service.py  │  ← Salva embedding
└────────┬────────┘
         │ save_face_embedding()
         │ pickle.dumps(array)
         ▼
┌─────────────────┐
│    Supabase     │  ← Armazena BYTEA
└─────────────────┘
```

### Fluxo 2: Reconhecimento

```
┌─────────────┐
│  Frontend   │  Captura foto da webcam
└──────┬──────┘
       │ POST /alunos/reconhecer
       │ {foto, turma_id, mode="smart"}
       ▼
┌──────────────────┐
│   alunos.py      │
└────────┬─────────┘
         │ get_turma_embeddings()
         ▼
┌──────────────────┐
│   db_service.py  │  Busca embeddings da turma
└────────┬─────────┘
         │ [{id: 1, embedding: [...]}]
         ▼
┌──────────────────┐
│hybrid_service.py │  ESTRATÉGIA SMART:
└────────┬─────────┘
         │
         │ 1) face_recognition (rápido)
         ├──────────┐
         │          │ Confiança >= 55%?
         │          └─→ SIM: Aceita ✅
         │
         │ 2) Confiança 35-55%?
         ├──────────┐
         │          │ Valida com DeepFace
         │          └─→ Concordam? ✅
         │
         │ 3) Fallback: DeepFace
         │
         ▼
┌──────────────────┐
│   db_service.py  │  registrar_presenca()
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    Supabase      │  INSERT presencas
└──────────────────┘
         │
         ▼
    Retorna JSON:
    {
      "status": "success",
      "aluno_id": 42,
      "confidence": 87.5,
      "method": "hybrid_validated"
    }
```

---

## 📊 Conceitos Avançados

### 1. Face Embeddings

**O que é um embedding facial?**

É uma representação matemática de um rosto em um espaço vetorial de alta dimensão (128D ou 512D).

```python
# Exemplo de embedding 128D
embedding = [
    0.123, -0.456, 0.789, ...,  # 128 números float
]

# Rostos similares = vetores próximos no espaço
pessoa1 = [0.1, 0.2, 0.3, ...]
pessoa1_outra_foto = [0.11, 0.19, 0.31, ...]  # Próximo!
pessoa2 = [0.9, -0.5, 0.1, ...]  # Distante!
```

**Como é gerado?**

1. **CNN (Convolutional Neural Network)** processa a imagem
2. **Extrai features** (olhos, nariz, formato do rosto)
3. **Reduz dimensionalidade** para 128D ou 512D
4. **Normaliza** o vetor

### 2. Métricas de Distância

**Distância Euclidiana:**
```python
import numpy as np

def euclidean_distance(v1, v2):
    return np.sqrt(np.sum((v1 - v2) ** 2))

# Exemplo
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
dist = euclidean_distance(a, b)  # 5.196
```

**Similaridade de Cosseno:**
```python
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# Retorna: -1 (opostos) até 1 (idênticos)
```

### 3. Async/Await no FastAPI

FastAPI suporta operações assíncronas:

```python
# Síncrono (bloqueia thread)
@router.post("/upload")
def upload_file(file: UploadFile):
    content = file.file.read()  # Bloqueia
    return {"size": len(content)}

# Assíncrono (não bloqueia)
@router.post("/upload")
async def upload_file(file: UploadFile):
    content = await file.read()  # Libera thread durante I/O
    return {"size": len(content)}
```

**Quando usar async:**
- ✅ Operações I/O (banco de dados, arquivos, APIs)
- ❌ Processamento CPU-intensivo (reconhecimento facial)

### 4. Middleware CORS

Permite requisições de outros domínios:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend
    allow_credentials=True,  # Cookies
    allow_methods=["*"],  # GET, POST, PUT, DELETE
    allow_headers=["*"],  # Authorization, Content-Type
)
```

**Por que é necessário?**

Navegadores bloqueiam requisições cross-origin por segurança (Same-Origin Policy). CORS permite exceções controladas.

---

## 🎓 Conceitos para Estudar

### 1. **RESTful API Design**
- GET: Buscar dados
- POST: Criar recursos
- PUT: Atualizar recursos
- DELETE: Deletar recursos

### 2. **ORM (Object-Relational Mapping)**
- Mapeia objetos Python → Tabelas SQL
- Vantagens: Type safety, queries legíveis
- SQLAlchemy é o ORM mais popular em Python

### 3. **Dependency Injection**
- FastAPI injeta dependências automaticamente
- Facilita testes (mock dependencies)
- Reduz acoplamento

### 4. **Deep Learning para Visão Computacional**
- CNNs extraem features de imagens
- Transfer learning: usar modelos pré-treinados
- Face recognition usa FaceNet, VGG-Face, ArcFace

### 5. **PostgreSQL e Índices**
- Índices aceleram buscas (B-Tree)
- Foreign keys garantem integridade referencial
- EXPLAIN ANALYZE para otimizar queries

---

## 🚀 Como Rodar o Backend

### 1. Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows PowerShell)
venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar .env

```bash
# Criar arquivo .env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-aqui
```

### 3. Rodar servidor

```bash
# Desenvolvimento (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Testar API

Abrir no navegador:
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

---

## 📚 Recursos de Estudo

### Documentação Oficial:
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **face_recognition**: https://github.com/ageitgey/face_recognition
- **DeepFace**: https://github.com/serengil/deepface

### Tutoriais:
- FastAPI com SQLAlchemy: https://fastapi.tiangolo.com/tutorial/sql-databases/
- Face Recognition tutorial: https://realpython.com/face-recognition-with-python/
- RESTful API design: https://restfulapi.net/

---

## ✅ Checklist de Conhecimentos

Após estudar este documento, você deve saber:

- [ ] Explicar arquitetura em camadas do backend
- [ ] Descrever schema do banco de dados e relacionamentos
- [ ] Entender como SQLAlchemy mapeia tabelas → classes
- [ ] Explicar o processo de extração de embeddings faciais
- [ ] Diferenciar face_recognition vs DeepFace
- [ ] Descrever a estratégia SMART do sistema híbrido
- [ ] Entender como funciona Dependency Injection no FastAPI
- [ ] Explicar o fluxo completo: cadastro → reconhecimento → presença
- [ ] Saber calcular distância euclidiana e similaridade de cosseno
- [ ] Configurar e rodar o servidor FastAPI

---

**Autor:** Documentação preparada para Senzaki (Backend)  
**Data:** Novembro 2025  
**Versão:** 1.0
