import face_recognition
import numpy as np
import json
from PIL import Image
import io

def get_face_encoding(file_bytes: bytes):
    img = Image.open(io.BytesIO(file_bytes))
    img = np.array(img)
    encodings = face_recognition.face_encodings(img)
    if len(encodings) == 0:
        return None
    return encodings[0].tolist()

def compare_encodings(enc1, enc2):
    e1 = np.array(enc1)
    e2 = np.array(enc2)
    distance = np.linalg.norm(e1 - e2)
    similarity = 1 / (1 + distance)  # simples métrica
    return round(similarity * 100, 2)
