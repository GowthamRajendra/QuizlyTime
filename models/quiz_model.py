from mongoengine import Document, IntField, StringField, ReferenceField, ListField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField, BooleanField

from models.question_model import Question

class AnsweredQuestion(EmbeddedDocument):
    question = ReferenceField(Question)
    user_answer = StringField()

class Quiz(Document):
    title = StringField(required=True)
    score = IntField(required=True)
    timestamp = DateTimeField(required=True)
    questions = ListField(ReferenceField(Question)) # questions in the quiz
    answered_questions = EmbeddedDocumentListField(AnsweredQuestion) # questions answered by user
    total_questions = IntField(default=10)
    user_created = BooleanField(default=False)

    meta = {'collection': 'singleplayer_quizzes'} # collection name in the database