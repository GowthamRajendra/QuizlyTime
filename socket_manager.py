from flask_socketio import SocketIO

socketio = SocketIO(async_mode='eventlet') # async_mode='eventlet' is needed for gunicorn to work with socketio
