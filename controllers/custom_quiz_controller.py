from flask import request, Blueprint, jsonify, make_response

from datetime import datetime 
import os

# import models
from models.user_model import User
from models.quiz_model import Quiz
from models.question_model import Question

# import service functions
from services.auth_service import token_required
from services.quiz_service import store_questions, create_quiz_questions
from services.custom_quiz_service import store_custom_quiz, get_stored_custom_quizzes, delete_stored_custom_quiz, edit_stored_custom_quiz, edit_stored_custom_quiz_title, begin_stored_quiz

custom_quiz_bp = Blueprint('custom_quiz_bp', __name__)

@custom_quiz_bp.after_request
def cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = os.getenv("FRONT_END_URL", 'http://localhost:5173')
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')

    return response

@custom_quiz_bp.route("/save-custom-quiz", methods=["POST"])
@token_required("access") 
def save_custom_quiz(user_data):
    questions = request.json.get('questions', [])
    title = request.json.get('title', "")

    # store questions in the database (can use same function as random quiz)
    questions = store_questions(questions)

    # save custom quiz to database and link it to the user
    store_custom_quiz(title, questions, user_data)

    # create quiz questions (same function as random quiz)
    quiz_questions = create_quiz_questions(questions)

    return make_response(jsonify(quiz_questions), 200)

@custom_quiz_bp.route("/get-custom-quizzes", methods=["GET"])
@token_required("access")
def get_custom_quizzes(user_data):
    
    response_data = get_stored_custom_quizzes()

    return make_response(jsonify(response_data), 200)

@custom_quiz_bp.route("/delete-custom-quiz", methods=["DELETE"])
@token_required("access")
def delete_custom_quiz(user_data):    
    quiz_id = request.json.get('quiz_id', "")

    delete_stored_custom_quiz(quiz_id, user_data)    

    return make_response(jsonify({"message": "Quiz deleted"}), 200)
    
# put request to update quiz title and questions
@custom_quiz_bp.route("/edit-custom-quiz", methods=["PUT"])
@token_required("access")
def edit_custom_quiz(user_data):
    quiz_id = request.json.get('quiz_id', "")
    title = request.json.get('title', "")

    new_questions = request.json.get('questions', [])
    
    quiz_questions = edit_stored_custom_quiz(quiz_id, title, new_questions, user_data)

    return make_response(jsonify(quiz_questions), 200)


# put request to update quiz title and send back questions
@custom_quiz_bp.route("/edit-custom-quiz-title", methods=["PUT"])
@token_required("access")
def edit_custom_quiz_title(user_data):
    quiz_id = request.json.get('quiz_id', "")
    title = request.json.get('title', "")

    new_questions = edit_stored_custom_quiz_title(quiz_id, title)
    
    return make_response(jsonify({"questions": new_questions}), 200)

@custom_quiz_bp.route("/begin-quiz", methods=["POST"])
@token_required("access")
def begin_quiz(user_data):
    quiz_id = request.json.get('quiz_id', "")

    begin_stored_quiz(quiz_id, user_data)

    return make_response(jsonify({"message": "Quiz started"}), 200)