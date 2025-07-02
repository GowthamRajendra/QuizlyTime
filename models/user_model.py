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

    def getUser(email):
        return User.objects(email=email).first()

    def getCreations(id):
        return User.objects(id=id).first().created_quizzes
    
    def getHistory(id):
        user = User.objects(id=id).first()

        history = sorted(user.completed_multi_quizzes + user.completed_single_quizzes, key=lambda q: q.timestamp, reverse=True)
    
        return history
                                                  
