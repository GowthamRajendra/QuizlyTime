from flask_socketio import SocketIO

# gevent needed for sockets to work on gunincorn
socketio = SocketIO(async_mode='gevent')
