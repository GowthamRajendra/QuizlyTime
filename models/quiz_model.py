from mongoengine import Document, IntField, StringField, ReferenceField, ListField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, BooleanField

from models.question_model import Question

class AnsweredQuestion(EmbeddedDocument):
    question = ReferenceField(Question)
    user_answer = StringField()

class Quiz(Document):
    score = IntField(required=True)
    timestamp = DateTimeField(required=True)
    answered_questions = ListField(EmbeddedDocumentField(AnsweredQuestion)) # questions answered by user
    total_questions = IntField(default=10)

    meta = {'collection': 'quizzes'} # collection name in the database