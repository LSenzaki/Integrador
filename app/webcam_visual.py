"""
webcam_visual.py
----------------
Teste de webcam mostrando a imagem em tempo real com reconhecimento facial.
"""
import cv2
from app.services.face_service import get_face_encoding, compare_encodings
from app.models.db_session import SessionLocal
from app.models import db_models
import json

# Conecta ao banco e busca alunos cadastrados
db = SessionLocal()
pessoas = db.query(db_models.Pessoa).all()
db.close()

if not pessoas:
    print("Nenhum aluno cadastrado.")
    exit()

# Lista de embeddings do banco
embeddings_db = [(p.id, p.nome, json.loads(p.embedding)) for p in pessoas]

# Inicia a webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível capturar a imagem da webcam")
        break

    # Reduz resolução para acelerar processamento
    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    # Extrai embedding
    encoding = get_face_encoding(cv2.imencode('.jpg', small_frame)[1].tobytes())

    if encoding:
        # Lista de resultados com similaridade
        resultados = []
        for pid, nome, emb in embeddings_db:
            sim = compare_encodings(emb, encoding)
            resultados.append({"nome": nome, "similaridade": sim})

        # Ordena pelo mais provável
        resultados = sorted(resultados, key=lambda x: x["similaridade"], reverse=True)
        top_result = resultados[0]

        # Mostra na imagem
        if top_result["similaridade"] > 50:  # limiar
            cv2.putText(frame, f"{top_result['nome']} ({top_result['similaridade']}%)",
                        (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # Exibe o frame
    cv2.imshow("Reconhecimento Facial", frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
