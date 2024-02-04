from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


# 定义事件处理程序
@socketio.on('connect')
def handle_connect():
    # 在客户端连接时触发
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    # 服务器断开时触发
    print('Client disconnected')


# 聊天室相关代码
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', f'User has joined the room: {room}', room=room)


@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('message', f'User has left the room: {room}', room=room)


@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    emit('message', message, room=room)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
