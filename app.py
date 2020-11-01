from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

global currentonlineusers
currentonlineusers = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main.js')
def get_handler_code():
    return render_template('main.js')

@app.route('/style.css')
def get_style_code():
    return render_template('style.css')

@app.route('/socketio.js')
def get_socket_code():
    return render_template('socketio.js')

@socketio.on('connection')
def new_connection(json):
    print('got ack')

@socketio.on('connect')
def new_user():
    global currentonlineusers
    currentonlineusers += 1
    emit('usercount', currentonlineusers, broadcast=True)
    print('new user connect')

@socketio.on('disconnect')
def user_disconnect():
    global currentonlineusers
    currentonlineusers -= 1
    emit('usercount', currentonlineusers, broadcast=True)
    print('user disconnected')

@socketio.on('newmessage')
def new_message(json):
    print('received json: ' + str(json))
    if json['username'] == '':
        json['username'] = 'Untitled User'
    emit('newmessage', json['username'] + ': ' + json['message'], broadcast=True)

if __name__ == '__main__':
    socketio.run(app)