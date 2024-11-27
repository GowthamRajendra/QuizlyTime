from mongoengine import Document, StringField, EmailField, ListField, ReferenceField

from src.models.quiz_model import Quiz

class User(Document):
    username = StringField(required=True, max_length=20)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    active_quiz = ReferenceField(Quiz) # quiz in progress
    completed_quizzes = ListField(ReferenceField(Quiz)) # list of completed quizzes
    created_quizzes = ListField(ReferenceField(Quiz)) # list of quizzes created by user
    
    meta = {'collection': 'users'} # collection name in the database
                                                  
