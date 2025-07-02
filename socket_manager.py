from flask_socketio import SocketIO

# gevent needed for sockets to work on gunincorn
# socketio = SocketIO(async_mode='gevent', message_queue='redis://localhost:6379/0')
socketio = SocketIO(async_mode='gevent')
