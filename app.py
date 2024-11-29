from flask import Flask
from mongoengine import connect
from dotenv import load_dotenv
# from flask_socketio import SocketIO, emit
from socket_manager import socketio

import os

# load environment variables from the .env file
load_dotenv()

DATABASE_URI = os.getenv('DB_URI')

# socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # set up config
    app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET")
    app.config['MONGO_URI'] = DATABASE_URI

    # import blueprints
    from controllers.user_controller import users_bp    
    from controllers.quiz_controller import quiz_bp
    from controllers.custom_quiz_controller import custom_quiz_bp

    # register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(custom_quiz_bp)

    # connect to the database
    connect('QuizAppDB', host=app.config['MONGO_URI'], uuidRepresentation="standard")

    # initialize socketio
    # change cors_allowed_origins later
    socketio.init_app(app, cors_allowed_origins='*')

    # @socketio.on('check_answer')
    # def test(data):
    #     print('checking answer')
    #     print(data)
    #     emit('answer_checked', data, broadcast=True)

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
