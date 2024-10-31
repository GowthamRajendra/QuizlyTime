from mongoengine import Document, StringField, EmailField, ListField, ReferenceField

from models.question_model import Question
from models.quiz_model import Quiz

class User(Document):
    username = StringField(required=True, max_length=20)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    # questions = ListField(ReferenceField(Question)) # list of questions of quiz taken by user
                                                    # might change to have session collections
                                                    # that stores questions for each session
    activeQuiz = ReferenceField(Quiz) # quiz in progress
    completedQuizzes = ListField(ReferenceField(Quiz)) # list of completed quizzes
    
    meta = {'collection': 'users'} # collection name in the database
                                                  
