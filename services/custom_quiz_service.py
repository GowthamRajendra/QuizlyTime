from datetime import datetime


from models.question_model import Question
from models.quiz_model import Quiz
from models.user_model import User

from services.quiz_service import create_quiz_questions


def store_custom_quiz(title, questions, user_data):
    # create quiz
    quiz = Quiz(title=title, score=0, timestamp=datetime.now(), total_questions=len(questions), questions=questions, user_created=True)
    quiz.save()

    # add quiz to user's created_quizzes
    user = User.objects(pk=user_data['sub']).first()
    user.created_quizzes.append(quiz)
    user.active_quiz = quiz
    user.save()

def get_stored_custom_quizzes():
    quizzes = Quiz.objects(user_created=True)

    print(quizzes)

    results = [
        {
            "id": str(quiz.id),
            "title": quiz.title,
            "timestamp": quiz.timestamp,
            "total_questions": quiz.total_questions,
            "questions": create_quiz_questions(quiz.questions)
        } for quiz in quizzes
    ]

    response_data = {
        "quizzes": results
    }

    return response_data

def delete_stored_custom_quiz(quiz_id, user_data):
    user = User.objects(pk=user_data['sub']).first()
    quiz = Quiz.objects(pk=quiz_id).first()

    user.created_quizzes.remove(quiz)
    user.save()

    quiz.delete()

def edit_stored_custom_quiz(quiz_id, title, new_questions, user_data):
    quiz = Quiz.objects(pk=quiz_id).first()
    quiz.title = title

    for question in new_questions:
        question_id = question.get('id', "")

        question_old = Question.objects(pk=question_id).first()

        question_old.prompt = question.get('question', "")
        question_old.category = question.get('category', "")
        question_old.difficulty = question.get('difficulty', "")
        question_old.type = question.get('type', "")
        question_old.correct_answer = question.get('correct_answer', "")
        question_old.incorrect_answers = question.get('incorrect_answers', [])
        question_old.save()

    quiz.save()

    # if user wants to take quiz after editing it
    user = User.objects(pk=user_data['sub']).first()
    user.active_quiz = Quiz.objects(pk=quiz_id).first()
    user.save()

    return create_quiz_questions(quiz.questions)

def edit_stored_custom_quiz_title(quiz_id, title):
    quiz = Quiz.objects(pk=quiz_id).first()
    quiz.title = title
    quiz.save()

    new_questions = []

    for question in quiz.questions:
        question_id = str(question.id)

        question_old = Question.objects(pk=question_id).first()

        new_questions.append({
            "question_id": question_id,
            "prompt": question_old.prompt,
            "category": question_old.category,
            "difficulty": question_old.difficulty,
            "type": question_old.type,
            "correct_answer": question_old.correct_answer,
            "incorrect_answers": question_old.incorrect_answers
        })
    
    return new_questions

def begin_stored_quiz(quiz_id, user_data):
    # setting user's active quiz
    quiz = Quiz.objects(pk=quiz_id).first()
    user = User.objects(pk=user_data['sub']).first()
    user.active_quiz = quiz
    user.save()
