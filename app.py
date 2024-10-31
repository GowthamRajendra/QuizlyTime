from flask import Flask
from mongoengine import connect
from dotenv import load_dotenv
from flask_socketio import SocketIO

import os


# load environment variables from the .env file
load_dotenv()

DATABASE_URI = os.getenv('DB_URI')

socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # set up config
    app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET")
    app.config['MONGO_URI'] = DATABASE_URI

    # import blueprints
    from controllers.user_controller import users_bp    
    from controllers.quiz_controller import quiz_bp

    # register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(quiz_bp)

    # connect to the database
    connect('QuizAppDB', host=app.config['MONGO_URI'])

    # initialize socketio
    # change cors_allowed_origins later
    socketio.init_app(app, cors_allowed_origins='*')

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True)
