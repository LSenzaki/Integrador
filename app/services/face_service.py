"""
face_service.py
---------------
Funções auxiliares para processamento facial usando a biblioteca face_recognition.

Funcionalidades:
- get_face_encoding: retorna o embedding do rosto a partir de uma imagem
- compare_encodings: calcula a similaridade entre dois embeddings
"""
import face_recognition
import numpy as np
from PIL import Image
import io

def get_face_encoding(file_bytes: bytes):
    """
    Retorna o embedding facial de uma imagem.
    Se não encontrar rosto, retorna None.
    """
    img = Image.open(io.BytesIO(file_bytes))
    img = np.array(img)
    encodings = face_recognition.face_encodings(img)
    if not encodings:
        return None
    return encodings[0].tolist()

def compare_encodings(enc1, enc2):
    """
    Calcula a similaridade entre dois embeddings faciais.
    
    Retorna:
    - Similaridade em porcentagem (float)
    """
    e1 = np.array(enc1)
    e2 = np.array(enc2)
    distancia = np.linalg.norm(e1 - e2)
    similarity = 1 / (1 + distancia)
    return round(similarity * 100, 2)
