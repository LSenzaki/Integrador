PROJETO DE RECONHECIMENTO FACIAL DOS ALUNOS DO BIOPARK

OBJETIVO
O objetivo é conseguir integrar um sistema automático de reconheciment odos alunos com o sistema usado pelos professores para automatizar o regiustro de presença dos alunos.

BIBLIOTECAS
Face Recognition

ESTRUTURA DO PROJETO

project_root/
│
├── app/                        # Código principal da aplicação FastAPI
│   ├── main.py                  # Ponto de entrada da aplicação
│   │
│   ├── routers/                 # Endpoints da API
│   │   ├── __init__.py
│   │   ├── faces.py             # Rotas de reconhecimento facial
│   │   └── students.py          # Rotas CRUD de estudantes e registros
│   │
│   ├── services/                # Regras de negócio
│   │   ├── __init__.py
│   │   ├── face_service.py      # Funções que utilizam face_recognition
│   │   └── db_service.py        # Operações com o banco de dados
│   │
│   ├── models/                  # Modelos do banco de dados
│   │   └── db_models.py         # Modelos SQLAlchemy
│   │
│   └── schemas/                 # Modelos de validação (Pydantic)
│       └── pydantic_schemas.py  # Schemas para entrada/saída da API
│
├── data/                        # Armazenamento de imagens
│   ├── known_faces/             # Fotos conhecidas (para encoding)
│   └── unknown_faces/           # Fotos capturadas via webcam
│
├── requirements.txt             # Dependências do projeto
├── Dockerfile                   # Arquivo para containerização (opcional)
└── README.md                    # Documentação do projeto


PROBLEMAS


CONCLUSÃO
