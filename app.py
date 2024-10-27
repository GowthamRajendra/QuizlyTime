from flask import Flask, jsonify, request
import requests
from html import unescape
from mongoengine import connect
from dotenv import load_dotenv
import os

from controllers.user_controller import users_bp

from models.user_model import User
from models.question_model import Question

# load environment variables from the .env file
load_dotenv()

DATABASE_URI = os.getenv('DB_URI')

app = Flask(__name__)

URL = "https://opentdb.com/api.php?"

# @app.route('/questions', methods=['GET'])
# def get_ques():
#     amount = request.json.get('amount')
#     type = request.json.get('type')
#     difficulty = request.json.get('difficulty')
#     category = request.json.get('category')

#     response = requests.get(URL + f'amount={amount}&category={category}&difficulty={difficulty}&type={type}').json()

#     questions = []

#     for ques in response["results"]:
#         ques["question"] = unescape(ques["question"])
#         ques["correct_answer"] = unescape(ques["correct_answer"])
#         for i in range(len(ques["incorrect_answers"])):
#             ques["incorrect_answers"][i] = unescape(ques["incorrect_answers"][i])

#         question = Question(category_name=ques["category"], 
#                      category_id=category, 
#                      difficulty=ques["difficulty"], 
#                      type=ques["type"], 
#                      question_text=ques["question"], 
#                      correct_answer=ques["correct_answer"], 
#                      incorrect_answers=ques["incorrect_answers"]
#                 )
        
#         question.save()
#         questions.append(question)
    
#     # print(response['results'])


#     # new user example
#     # user = User(name='test2', email='test2@mail.ca', password='password', questions=questions)
#     # user.save()


#     # updating existing user example
#     user_existing = User.objects(email='test2@mail.ca').first()

#     # delete existing questions from questions collection
#     for question in user_existing.questions:
#         print('deleting question: ', question.question_text)

#         question.delete()

#     user_existing.questions = questions
#     user_existing.save()
     


#     return jsonify(response)

def create_app():
    app = Flask(__name__)

    # set up config
    app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET")
    app.config['MONGO_URI'] = DATABASE_URI

    # register blueprints
    app.register_blueprint(users_bp)

    # connect to the database
    connect('QuizAppDB', host=app.config['MONGO_URI'])

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
