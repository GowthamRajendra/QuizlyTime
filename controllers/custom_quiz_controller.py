from flask import request, Blueprint, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests

from datetime import datetime 

# import models
from models.user_model import User
from models.quiz_model import Quiz
from models.question_model import Question
from models.quiz_model import AnsweredQuestion

# import service functions
from services.auth_service import access_token_required
from services.quiz_service import store_questions, create_quiz_questions

quiz_bp = Blueprint('quiz_bp', __name__)
# CORS(quiz_bp, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})

@quiz_bp.after_request
def cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@quiz_bp.route("/custom-quiz", methods=["POST", "OPTIONS"])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'], supports_credentials=True)
@access_token_required 
def custom_quiz(user_data):
    print(request.method)
    questions = request.json.get('questions', [])
    title = request.json.get('title', "")

    # store questions in the database (can use same function as random quiz)
    questions = store_questions(questions)

    # create quiz
    quiz = Quiz(title=title, score=0, timestamp=datetime.now(), total_questions=len(questions), questions=questions)
    quiz.save()

    # add quiz to user's created_quizzes
    user = User.objects(pk=user_data['sub']).first()
    user.created_quizzes.append(quiz)
    user.save()

    # create quiz questions (same function as random quiz)
    quiz_questions = create_quiz_questions(questions)

    return make_response(jsonify(quiz_questions), 200)
