from html import unescape
import random
from datetime import datetime

from models.question_model import Question
from models.quiz_model import Quiz, AnsweredQuestion
from models.user_model import User

from llm_manager import reword_question

# dictionary to map category id to category name
# needed for title of random quizzes
category_dict = {
    '': 'Any Category',
    '9': "General Knowledge",
    '10': "Entertainment: Books",
    '11': "Entertainment: Film",
    '12': "Entertainment: Music",
    '13': "Entertainment: Musicals & Theatres",
    '14': "Entertainment: Television",
    '15': "Entertainment: Video Games",
    '16': "Entertainment: Board Games",
    '17': "Science & Nature",
    '18': "Science: Computers",
    '19': "Science: Mathematics",
    '20': "Mythology",
    '21': "Sports",
    '22': "Geography",
    '23': "History",
    '24': "Politics",
    '25': "Art",
    '26': "Celebrities",
    '27': "Animals",
    '28': "Vehicles",
    '29': "Entertainment: Comics",
    '30': "Science: Gadgets",
    '31': "Entertainment: Japanese Anime & Manga",
    '32': "Entertainment: Cartoon & Animations"
}

def store_random_quiz(questions, category, user_data, amount):
    # create a new quiz object and store it in the database
    # set timestamp to the current time since the quiz is just starting
    quiz = Quiz(title=category_dict[category], score=0, timestamp=datetime.now(), total_questions=amount, questions=questions)
    quiz.save()

    # set the active_quiz field of the user to the quiz object
    user = User.objects(pk=user_data['sub']).first()
    user.active_quiz = quiz
    user.save()

    quiz_questions = create_quiz_questions(questions)

    return quiz_questions

def check_question(data):
    # using the user's email from the client side 
    # while fixing the token issues
    # user = User.objects(pk=user_data['sub']).first()
    user = User.objects(email=data['email']).first()
    quiz = user.active_quiz
    question_index = data['question_index']

    # print(data)
    # print('quiz', quiz.id, 'for user', user.username)
    # print("active quiz", user.active_quiz)
    # print(f"Type of quiz: {type(quiz)}")
    # print(f"Quiz before the if check: {quiz}")
    # print(f"Is quiz falsy? {not quiz}")

    # dont check the answer if the user doesn't have an active quiz
    if quiz is None:
        print("no active quiz")
        return

    # get the question object from the question id
    question = Question.objects(pk=data['question_id']).first()
    print(question.category)

    # check if the answer is correct
    if data['user_answer'] == question.correct_answer:
        print(question.correct_answer)
        
        # scale points to time left
        if data["time_left"] / data["max_time"] > 0.75:
            quiz.score += 10
        else:
            quiz.score += 10 * (data["time_left"] / data["max_time"])

    # store the question and user's answer in the answered_questions list
    quiz.answered_questions.append(
        AnsweredQuestion(question=question, user_answer=data['user_answer'])
    )

    quiz.save() 

    results = {
        "correct_answer": question.correct_answer,
        "question_index": question_index,
    }

    return results, quiz, user

def store_completed_quiz(quiz, user):
    if quiz.user_created:
    # create copy of quiz for user
        quiz_history = Quiz(
            title=quiz.title, 
            score=quiz.score, 
            timestamp=datetime.now(), 
            total_questions=quiz.total_questions, 
            questions=quiz.questions,
            answered_questions=quiz.answered_questions
        )
        quiz_history.save()
        user.completed_quizzes.append(quiz_history)

        # reset original quiz
        quiz.answered_questions = []
        quiz.score = 0
        quiz.save()

    else:
        # add quiz to user's completed quizzes
        user.completed_quizzes.append(quiz)

    user.active_quiz = None
    user.save()


def create_quiz_questions(questions_list):
    quiz_questions = []

    for question in questions_list:
        # shuffle the choices
        choices = [question.correct_answer] + question.incorrect_answers
        random.shuffle(choices)

        # dont shuffle the choices for boolean questions
        if question.type == "boolean":
            choices = ["True", "False"]

        # timer based on difficulty
        if question.difficulty == "easy":
            timer = 10
        elif question.difficulty == "medium":
            timer = 15
        else:
            timer = 20

        quiz_questions.append({
            "question_id": str(question.id),
            "prompt": question.prompt,
            "category": question.category,
            "difficulty": question.difficulty,
            "type": question.type,
            "choices": choices,
            "timer": timer
        })

    return quiz_questions


def store_questions(questions, custom):
    questions_list = []

    for i, ques in enumerate(questions):
        # unescape html entities. removes &quot;, &amp;, etc.
        ques["question"] = unescape(ques["question"])
        ques["correct_answer"] = unescape(ques["correct_answer"])
        ques["category"] = unescape(ques["category"])
        for i in range(len(ques["incorrect_answers"])):
            ques["incorrect_answers"][i] = unescape(ques["incorrect_answers"][i])

        # reword if less than 5 ques or every 5th question 
        # because LLM is very slow
        if not custom and ques["type"] != "boolean" and (i % 5 == 0 or len(questions) <= 5):
            reworded_question = reword_question(
                                    ques["question"], 
                                    ques["correct_answer"], 
                                    ques["incorrect_answers"]
                                )
            if reworded_question:
                ques["question"] = reworded_question["question"]
                ques["correct_answer"] = reworded_question["correct_answer"]
                ques["incorrect_answers"] = reworded_question["incorrect_answers"]

        question = Question(category=ques["category"], 
                    #  category_id=category_dict[ques["category"]],
                     difficulty=ques["difficulty"], 
                     type=ques["type"], 
                     prompt=ques["question"], 
                     correct_answer=ques["correct_answer"], 
                     incorrect_answers=ques["incorrect_answers"]
                )
        
        question.save()
        questions_list.append(question)
    
    return questions_list