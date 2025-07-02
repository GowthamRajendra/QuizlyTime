from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, IntField, StringField, ReferenceField, ListField, DateTimeField, BooleanField, ObjectIdField
from bson import ObjectId

from models.question_model import Question
from models.quiz_model import AnsweredQuestion


class MultiplayerParticipant(EmbeddedDocument):
    user = ReferenceField('User', required=True)
    answered_questions = EmbeddedDocumentListField(AnsweredQuestion)
    score = IntField(default=0)
    is_finished = BooleanField(default=False)

class MultiplayerQuiz(Document):
    title = StringField(required=True)
    questions = ListField(ReferenceField(Question))
    timestamp = DateTimeField(required=True)
    total_questions = IntField(default=10)

    participants = EmbeddedDocumentListField(MultiplayerParticipant)

    meta = {'collection': 'multiplayer_quizzes'}

    def getQuiz(quiz_id):
        return MultiplayerQuiz.objects(id=quiz_id).first()

    def getParticipant(self, user_id):
        # need to convert because participant.user.id is a 
        obj_user_id = ObjectId(user_id)
        for participant in self.participants:
            if participant.user.id == obj_user_id:
                return participant
        
        return None
    
    def getAllParticipants(self):
        return self.participants

