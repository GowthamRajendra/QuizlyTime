from flask_socketio import SocketIO
import os

# gevent needed for sockets to work on gunincorn
socketio = SocketIO(async_mode='eventlet', message_queue=f'{os.getenv("REDIS_URL", "redis://localhost:6379")}/0')
# socketio = SocketIO(async_mode='gevent')
