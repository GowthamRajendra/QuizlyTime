from mongoengine import Document, StringField, EmailField, ListField, ReferenceField, GenericReferenceField

from models.quiz_model import Quiz

class User(Document):
    username = StringField(required=True, max_length=20)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    active_quiz = GenericReferenceField() # quiz in progress, generic because it can be either Quiz or MultiplayerQuiz
    completed_single_quizzes = ListField(ReferenceField(Quiz)) # list of completed singleplayer quizzes
    completed_multi_quizzes = ListField(ReferenceField('MultiplayerQuiz')) # list of completed multiplayer quizzes
    created_quizzes = ListField(ReferenceField(Quiz)) # list of quizzes created by user
    
    meta = {'collection': 'users'} # collection name in the database
                                                  
