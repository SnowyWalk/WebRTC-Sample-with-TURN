from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}
global A, B
A = None
B = None

@socketio.on('connect')
def handle_connect():
    global A, B
    # 클라이언트가 연결되면 socket id를 추적
    clients[request.sid] = request.sid
    if A is None:
        A = request.sid
        emit('msg', 'you are A', room=request.sid)
        print(f"Client connected: {request.sid} => A")
    else:
        B = request.sid
        emit('msg', 'you are B', room=request.sid)
        print(f"Client connected: {request.sid} => B")

@socketio.on('disconnect')
def handle_disconnect():
    global A, B
    # 클라이언트가 연결을 끊으면 해당 소켓 ID 제거

    if A == request.sid:
        A = None
    elif B == request.sid:
        B = None

    if request.sid in clients:
        del clients[request.sid]
        print(f"Client disconnected: {request.sid}")

@app.route('/')
def index():
    import os
    print(os.getcwd())
    # 현재 디렉토리를 이 파일이 있는 위치로 변경
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(os.getcwd())
    # return render_template('C:\sejun\WebRTC (Flask)\index.html')  # 클라이언트가 접속할 기본 HTML 파일
    return render_template('index.html')  # 클라이언트가 접속할 기본 HTML 파일

@socketio.on('offer')
def handle_offer(offer):
    global A, B
    if A == request.sid:
        print("A -> B offer")
        emit('offer', offer, room=B)
    elif B == request.sid:
        print("B -> A offer")
        emit('offer', offer, room=A)

@socketio.on('answer')
def handle_answer(answer):
    global A, B
    if A == request.sid:
        print("A -> B answer")
        emit('answer', answer, room=B)
    elif B == request.sid:
        print("B -> A answer")
        emit('answer', answer, room=A)

@socketio.on('ice_candidate')
def handle_ice_candidate(candidate):
    global A, B
    if A == request.sid:
        print("A -> B ICE candidate")
        emit('ice_candidate', candidate, room=B)
    elif B == request.sid:
        print("B -> A ICE candidate")
        emit('ice_candidate', candidate, room=A)

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
