import cv2
import requests

# Configurações do servidor
SERVER_URL = 'http://localhost:3001/api/update'

def update_server(people_in, people_out, people_inside):
    try:
        response = requests.post(SERVER_URL, json={
            'peopleIn': people_in,
            'peopleOut': people_out,
            'peopleInside': people_inside
        })
        response.raise_for_status()
    except Exception as e:
        print(f"Erro ao atualizar o servidor: {e}")

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

    # Posição da linha vertical para contagem de pessoas (em pixels)
    line_position = 320  # Posição X da linha vertical

    # Contadores
    people_in = 0
    people_out = 0
    people_inside = 0

    # Lista para armazenar as posições anteriores dos rostos
    previous_faces = {}

    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar o frame.")
                break

            # Redimensiona a imagem (opcional)
            frame = cv2.resize(frame, (640, 480))

            # Converte a imagem para escala de cinza para a detecção de rostos
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detecção de rostos
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            current_faces = {}

            for i, (x, y, w, h) in enumerate(faces):
                # Desenha o retângulo ao redor do rosto
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Identificação única do rosto atual
                current_faces[i] = (x, x + w)

                # Verifica se o rosto foi visto anteriormente
                if i in previous_faces:
                    prev_x_min, prev_x_max = previous_faces[i]
                    curr_x_min, curr_x_max = current_faces[i]

                    # Verifica se o rosto cruzou a linha vertical completamente
                    if prev_x_max <= line_position and curr_x_max > line_position:
                        people_in += 1
                        people_inside += 1
                    elif prev_x_min >= line_position and curr_x_min < line_position:
                        people_out += 1
                        people_inside -= 1

            update_server(people_in, people_out, people_inside)
            # Atualiza as posições anteriores com as atuais
            previous_faces = current_faces

            # Desenha a linha vertical no frame
            cv2.line(frame, (line_position, 0), (line_position, frame.shape[0]), (255, 0, 0), 2)

            # Exibe os dados na tela
            cv2.putText(frame, f'Entradas: {people_in}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Saidas: {people_out}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f'Dentro: {people_inside}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Mostra o vídeo com as detecções
            cv2.imshow('Contador de Pessoas', frame)

            # Pressione 'q' para sair
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"Erro durante a execução: {e}")
            break

    # Libera a captura e fecha as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

