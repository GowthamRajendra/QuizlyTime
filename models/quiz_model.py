from mongoengine import Document, IntField, StringField, ReferenceField, ListField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField

from models.question_model import Question

class AnsweredQuestion(EmbeddedDocument):
    question = ReferenceField(Question)
    user_answer = StringField()

class Quiz(Document):
    score = IntField(required=True)
    timestamp = DateTimeField(required=True)
    answered_questions = ListField(EmbeddedDocumentField(AnsweredQuestion)) # questions answered by user

    meta = {'collection': 'quizzes'} # collection name in the database