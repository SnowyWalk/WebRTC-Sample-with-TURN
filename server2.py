from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

clients = []

def get_other_id(sid):
    return (clients[1] if len(clients) > 1 else '') if sid == clients[0] else clients[0]

@socketio.on('connect')
def handle_connect():
    # 클라이언트가 연결되면 socket id를 추적
    print(clients, '->', request.sid)
    clients.append(request.sid)
    for client in clients:
        emit('ID', {'myid': client, 'otherid': get_other_id(client)}, room=client)
    print(clients)

@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)
    for client in clients:
        emit('ID', {'myid': client, 'otherid': get_other_id(client)}, room=client)

@app.route('/')
def index():
    return render_template('index2.html')  # 클라이언트가 접속할 기본 HTML 파일

@socketio.on('offer')
def handle_offer(offer):
    emit('offer', offer, room=get_other_id(request.sid))

@socketio.on('answer')
def handle_answer(answer):
    emit('answer', answer, room=get_other_id(request.sid))

@socketio.on('ice_candidate')
def handle_ice_candidate(candidate):
    print('ice_candidate', request.sid, get_other_id(request.sid))
    emit('ice_candidate', candidate, room=get_other_id(request.sid))

@app.route('/ice')
def ice():
    return jsonify({
        "iceServers": [
            {"urls": "stun:127.0.0.1:3478"},
            {"urls": "turn:127.0.0.1:3478"}
        ]
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)
