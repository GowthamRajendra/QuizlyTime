from flask import Flask, jsonify, request
import requests
from html import unescape
from mongoengine import connect
from dotenv import load_dotenv
import os

from controllers.user_controller import users_bp
from controllers.quiz_controller import quiz_bp

from models.user_model import User
from models.question_model import Question

# load environment variables from the .env file
load_dotenv()

DATABASE_URI = os.getenv('DB_URI')


def create_app():
    app = Flask(__name__)

    # set up config
    app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET")
    app.config['MONGO_URI'] = DATABASE_URI

    # register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(quiz_bp)

    # connect to the database
    connect('QuizAppDB', host=app.config['MONGO_URI'])

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
