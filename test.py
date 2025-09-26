import face_recognition
import cv2
import os
import numpy as np

# Caminho para a pasta de faces conhecidas
KNOWN_FACES_DIR = "data/known_faces"

# Inicializa listas para armazenar encodings e nomes
known_face_encodings = []
known_face_names = []

# Carrega todas as imagens da pasta known_faces
for name in os.listdir(KNOWN_FACES_DIR):
    person_dir = os.path.join(KNOWN_FACES_DIR, name)
    if not os.path.isdir(person_dir):
        continue
    for filename in os.listdir(person_dir):
        filepath = os.path.join(person_dir, filename)
        image = face_recognition.load_image_file(filepath)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)

print(f"{len(known_face_names)} alunos carregados: {known_face_names}")

# Inicializa webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    # Reduz tamanho para aumentar velocidade
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detecta faces
    face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Compara com faces conhecidas
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        name = "Desconhecido"
        distance = 1.0

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            distance = face_distances[best_match_index]
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        face_names.append(f"{name} ({distance:.2f})")

    # Desenha quadrados e nomes
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Ajusta para tamanho original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)

    cv2.imshow('Reconhecimento Facial', frame)

    # Sai com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
