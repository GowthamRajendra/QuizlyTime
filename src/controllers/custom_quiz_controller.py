from flask import request, Blueprint, jsonify, make_response
import requests

from datetime import datetime 

# import models
from src.models.user_model import User
from src.models.quiz_model import Quiz
from src.models.question_model import Question
from src.models.quiz_model import AnsweredQuestion

# import service functions
from src.services.auth_service import access_token_required
from src.services.quiz_service import store_questions, create_quiz_questions

custom_quiz_bp = Blueprint('custom_quiz_bp', __name__)

@custom_quiz_bp.after_request
def cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@custom_quiz_bp.route("/custom-quiz", methods=["POST"])
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
    user.active_quiz = quiz
    user.save()

    # create quiz questions (same function as random quiz)
    quiz_questions = create_quiz_questions(questions)

    return make_response(jsonify(quiz_questions), 200)
