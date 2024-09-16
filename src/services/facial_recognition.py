import cv2
import requests
import pickle
import socketio
import os
from dotenv import load_dotenv


load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")

# Inicializar socketio cliente
sio = socketio.Client()

# Conectar ao servidor Socket.IO
sio.connect("http://localhost:3001")

def main():
    # Carrega o classificador Haar Cascade para detecção de rostos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    if face_cascade.empty():
        print("Erro ao carregar o classificador Haar Cascade.")
        return

    # Captura de vídeo da webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a captura de vídeo.")
        return

    line_position = 320  # Posição X da linha vertical
    people_in, people_out, people_inside = 0, 0, 0
    previous_faces = {}

    while True:
        try:

            old_people_in = people_in
            old_people_out = people_out
            old_people_inside = people_inside

            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar o frame.")
                break

            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            current_faces = {}
            for i, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                current_faces[i] = (x, x + w)

                if i in previous_faces:
                    prev_x_min, prev_x_max = previous_faces[i]
                    curr_x_min, curr_x_max = current_faces[i]

                    if prev_x_max <= line_position and curr_x_max > line_position:
                        people_in += 1
                        people_inside += 1
                    elif prev_x_min >= line_position and curr_x_min < line_position:
                        people_out += 1
                        people_inside -= 1

            # update_server(people_in, people_out, people_inside)
            previous_faces = current_faces
            cv2.line(frame, (line_position, 0), (line_position, frame.shape[0]), (255, 0, 0), 2)
            cv2.putText(frame, f'Entradas: {people_in}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Saidas: {people_out}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f'Dentro: {people_inside}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Enviar dados para o servidor via socketio

            if(old_people_in != people_in or old_people_out != people_out or old_people_inside != people_inside):
              sio.emit('people_data', {
                  'peopleIn': people_in,
                  'peopleOut': people_out,
                  'peopleInside': people_inside
              })

            cv2.imshow('Contador de Pessoas', frame)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"Erro durante a execução: {e}")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()