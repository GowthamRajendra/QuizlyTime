from flask import request, Blueprint, jsonify, make_response
import requests
from flask_socketio import emit
import os
# import json

# import service functions
from services.auth_service import token_required
from services.quiz_service import store_questions, store_random_quiz, check_question, store_completed_quiz

from socket_manager import socketio 

quiz_bp = Blueprint('quiz_bp', __name__)

# CORS headers, needed for jwt to work
@quiz_bp.after_request
def cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = os.getenv("FRONT_END_URL", 'http://localhost:5173')
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# get quiz questions from the API
@quiz_bp.route("/quiz", methods=["POST"])
@token_required("access") 
def create_random_quiz(user_data):
    amount = request.json.get('amount', 10)
    type = request.json.get('type', "")
    difficulty = request.json.get('difficulty', "")
    category = request.json.get('category', "")

    # empty string for the query param are handled by the API, treats them as if they weren't included
    API_URL = f'https://opentdb.com/api.php?amount={amount}&type={type}&difficulty={difficulty}&category={category}'

    response = requests.get(API_URL).json()

    # with open('original.json', 'w') as f:
    #     ques_dicts = []
    #     for question in response.get('results'):
    #         question_dict = {}
    #         question_dict["question"] = question.get('question')
    #         question_dict["correct_answer"] = question.get('correct_answer')
    #         question_dict["incorrect_answers"] = question.get('incorrect_answers')
    #         ques_dicts.append(question_dict)

    #     json.dump(ques_dicts, f, indent=4)

    print(response)

    # store the questions in the database, and return the question objects as a list
    questions = store_questions(response['results'], False)

    # with open('reworded.json', 'w') as f:
    #     ques_dicts = []
    #     for question in questions:
    #         question_dict = {}
    #         question_dict["question"] = question.prompt
    #         question_dict["correct_answer"] = question.correct_answer
    #         question_dict["incorrect_answers"] = question.incorrect_answers
    #         ques_dicts.append(question_dict)

    #     json.dump(ques_dicts, f, indent=4)
    
    # create and store random quiz
    quiz_questions = store_random_quiz(questions, category, user_data, amount)
    
    print(quiz_questions)

    # return the quiz
    return make_response(jsonify(quiz_questions), 200)

@socketio.on('connect')
def test_connect():
    print('connected')

@socketio.on('disconnect')
def test_disconnect():
    print('disconnected')

# check the user's answer and send result back to the client
@socketio.on('check_answer')
def check_answer(data):
    results, quiz, user = check_question(data)

    # print("results", results)

    emit('answer_checked', results)

    # check if the quiz is completed
    # send the score back to the client and store results in the database
    print("in controller", len(quiz.answered_questions), quiz.total_questions)
    if len(quiz.answered_questions) == quiz.total_questions:
        print('quiz completed', quiz.score)
        emit('quiz_completed', {"score": quiz.score})

        store_completed_quiz(quiz, user)
