import face_recognition
import numpy as np
from PIL import Image
import io

def get_face_encoding(file_bytes: bytes):
    img = Image.open(io.BytesIO(file_bytes))
    img = np.array(img)
    encodings = face_recognition.face_encodings(img)
    if not encodings:
        return None
    return encodings[0].tolist()

def compare_encodings(enc1, enc2):
    e1 = np.array(enc1)
    e2 = np.array(enc2)
    distancia = np.linalg.norm(e1 - e2)
    similarity = 1 / (1 + distancia)
    return round(similarity * 100, 2)
