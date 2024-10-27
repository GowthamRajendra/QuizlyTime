from mongoengine import Document, StringField, IntField, ListField

class Question(Document):
    category_name = StringField(required=True) # api accepts integer but store name as well
    category_id = IntField(required=True)
    difficulty = StringField(required=True)
    type = StringField(required=True)
    question_text = StringField(required=True)
    correct_answer = StringField(required=True)
    incorrect_answers = ListField(StringField(), required=True)

    meta = {'collection': 'questions'} # collection name in the database