from html import unescape
import random

from models.question_model import Question

# prepare questions into format for frontend quiz game play and return them
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

# transform and store questions in the db and return list of question objects
def store_questions(questions):
    questions_list = []

    for ques in questions:
        # unescape html entities. removes &quot;, &amp;, etc.
        ques["question"] = unescape(ques["question"])
        ques["correct_answer"] = unescape(ques["correct_answer"])
        ques["category"] = unescape(ques["category"])
        for i in range(len(ques["incorrect_answers"])):
            ques["incorrect_answers"][i] = unescape(ques["incorrect_answers"][i])

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