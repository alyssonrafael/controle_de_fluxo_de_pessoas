from dotenv import load_dotenv
import socketio
from flask import Flask, jsonify

# Carregar variáveis de ambiente
load_dotenv()

# Inicializando socketio e Flask
sio = socketio.Server(cors_allowed_origins='*')
app = Flask(__name__)

# Conectando socketio ao Flask
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.on('people_data')  # Nome do evento que o microserviço envia
def handle_people_data(sid, data):
    print('Dados recebidos do microserviço:', data)

    # Agora emitimos esses dados para o front-end
    sio.emit('update_frontend', data)  # Enviar para o front-end com o evento 'update_frontend'

if __name__ == '__main__':
    # Executar o servidor Flask com socketio na porta desejada (ex: 5000)
    app.run(host='0.0.0.0', port=3001)
