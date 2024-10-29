from flask import request, Blueprint, jsonify, make_response
from html import unescape
import requests

from models.user_model import User
from models.question_model import Question

from services.auth_service import token_required

quiz_bp = Blueprint('quiz_bp', __name__)

# easiest way right now, might change later
category_dict = {
    "General Knowledge": 9,
    "Entertainment: Books": 10,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Musicals & Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Science: Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Entertainment: Comics": 29,
    "Science: Gadgets": 30,
    "Entertainment: Japanese Anime & Manga": 31,
    "Entertainment: Cartoon & Animations": 32
}

@quiz_bp.after_request
def cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@quiz_bp.route("/quiz", methods=["POST"])
@token_required
def get_quiz_questions(user_data):
    amount = request.json.get('amount', 10)
    type = request.json.get('type', "")
    difficulty = request.json.get('difficulty', "")
    category = request.json.get('category', "")

    print('amount: ', amount)
    print('type: ', type)
    print('difficulty: ', difficulty)
    print('category: ', category)

    # empty string for the query param are handled by the API, treats them as if they weren't included
    API_URL = f'https://opentdb.com/api.php?amount={amount}&type={type}&difficulty={difficulty}&category={category}'

    response = requests.get(API_URL).json()

    questions = []

    for ques in response["results"]:
        # unescape html entities
        ques["question"] = unescape(ques["question"])
        ques["correct_answer"] = unescape(ques["correct_answer"])
        ques["category"] = unescape(ques["category"])
        for i in range(len(ques["incorrect_answers"])):
            ques["incorrect_answers"][i] = unescape(ques["incorrect_answers"][i])

        question = Question(category_name=ques["category"], 
                     category_id=category_dict[ques["category"]],
                     difficulty=ques["difficulty"], 
                     type=ques["type"], 
                     question_text=ques["question"], 
                     correct_answer=ques["correct_answer"], 
                     incorrect_answers=ques["incorrect_answers"]
                )
        
        question.save()
        questions.append(question)
    
    # print(response['results'])

    user = User.objects(pk=user_data['sub']).first()

    # delete existing questions from questions collection
    for question in user.questions:
        print('deleting question: ', question.question_text)

        question.delete()

    user.questions = questions
    user.save()
     
    return make_response(jsonify(response), 200)