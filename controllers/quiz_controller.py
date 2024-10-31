from flask import request, Blueprint, jsonify, make_response
import requests
from flask_socketio import emit

from datetime import datetime 

# import models
from models.user_model import User
from models.quiz_model import Quiz
from models.question_model import Question

# import service functions
from services.auth_service import access_token_required
from services.quiz_service import store_questions, create_quiz_questions

from models.quiz_model import AnsweredQuestion

from socket_manager import socketio 

quiz_bp = Blueprint('quiz_bp', __name__)

# dont need it for now
# category_dict = {
#     "General Knowledge": 9,
#     "Entertainment: Books": 10,
#     "Entertainment: Film": 11,
#     "Entertainment: Music": 12,
#     "Entertainment: Musicals & Theatres": 13,
#     "Entertainment: Television": 14,
#     "Entertainment: Video Games": 15,
#     "Entertainment: Board Games": 16,
#     "Science & Nature": 17,
#     "Science: Computers": 18,
#     "Science: Mathematics": 19,
#     "Mythology": 20,
#     "Sports": 21,
#     "Geography": 22,
#     "History": 23,
#     "Politics": 24,
#     "Art": 25,
#     "Celebrities": 26,
#     "Animals": 27,
#     "Vehicles": 28,
#     "Entertainment: Comics": 29,
#     "Science: Gadgets": 30,
#     "Entertainment: Japanese Anime & Manga": 31,
#     "Entertainment: Cartoon & Animations": 32
# }

@quiz_bp.after_request
def cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@quiz_bp.route("/quiz", methods=["POST"])
@access_token_required 
def get_quiz_questions(user_data):
    amount = request.json.get('amount', 10)
    type = request.json.get('type', "")
    difficulty = request.json.get('difficulty', "")
    category = request.json.get('category', "")

    # empty string for the query param are handled by the API, treats them as if they weren't included
    API_URL = f'https://opentdb.com/api.php?amount={amount}&type={type}&difficulty={difficulty}&category={category}'

    response = requests.get(API_URL).json()

    # store the questions in the database, and return the question objects as a list
    questions = store_questions(response['results'])
    
    # create a new quiz object and store it in the database
    # set timestamp to the current time since the quiz is just starting
    quiz = Quiz(score=0, timestamp=datetime.now(), total_questions=amount)
    quiz.save()

    # set the activeQuiz field of the user to the quiz object
    user = User.objects(pk=user_data['sub']).first()
    user.activeQuiz = quiz
    user.save()

    # # delete existing questions from questions collection
    # for question in user.questions:
    #     print('deleting question: ', question.prompt)

    #     question.delete()

    # user.questions = questions
    # user.save()

    quiz_questions = create_quiz_questions(questions)
     
    # return the first question to start the quiz
    return make_response(jsonify(quiz_questions), 200)


# @socketio.on('check_answer')
# def test(data):
#     print('checking answer')
#     print(data)
#     emit('answer_checked', data, broadcast=True)

# TODO: fix the token issues
@socketio.on('check_answer')
def check_answer(data):
    # using the user's email from the client side 
    # while fixing the token issues
    # user = User.objects(pk=user_data['sub']).first()
    user = User.objects(email=data['email']).first()
    quiz = user.activeQuiz

    # dont check the answer if the user doesn't have an active quiz
    if not quiz:
        return

    # get the question object from the question id
    question = Question.objects(pk=data['question_id']).first()

    # check if the answer is correct
    if data['user_answer'] == question.correct_answer:
        print(question.correct_answer)
        quiz.score += 1

    # store the question and user's answer in the answered_questions list
    quiz.answered_questions.append(
        AnsweredQuestion(question=question, user_answer=data['user_answer'])
    )

    quiz.save() 

    results = {
        "correct_answer": question.correct_answer
    }

    emit('answer_checked', results)

    # check if the quiz is completed
    if len(quiz.answered_questions) == quiz.total_questions:
        emit('quiz_completed', {"score": quiz.score})
        user.activeQuiz = None
        user.save()

