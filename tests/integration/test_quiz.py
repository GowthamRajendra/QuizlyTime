# Test cases for quiz routes
# Routes are in ./controllers/quiz_controller.py

import time

# test creation of random quiz
# 10 questions, any category, any type and any difficulty
def test_create_random_quiz_default(authenticated_client):
    data = {
        "amount": 10,
        "category": "",
        "type": "",
        "difficulty": ""
    }

    # API has a rate limit of 1 request per 5 seconds
    time.sleep(5)
    response = authenticated_client.post("/quiz", json=data)

    assert response.status_code == 200
    assert len(response.json) == 10

    for question in response.json:
        assert "question_id" in question
        assert "prompt" in question
        assert "category" in question
        assert "difficulty" in question
        assert "type" in question
        assert "choices" in question
        assert "timer" in question

        assert question["timer"] in [10, 15, 20]

def test_create_random_quiz_with_params(authenticated_client):
    data = {
        "amount": 5,
        "category": "15",
        "type": "multiple",
        "difficulty": "hard"
    }

    # API has a rate limit of 1 request per 5 seconds
    time.sleep(5)

    response = authenticated_client.post("/quiz", json=data)

    assert response.status_code == 200
    assert len(response.json) == 5

    for question in response.json:
        assert "question_id" in question
        assert "prompt" in question
        assert "category" in question
        assert "difficulty" in question
        assert "type" in question
        assert "choices" in question
        assert "timer" in question

        assert question["category"] == "Entertainment: Video Games"
        assert question["difficulty"] == "hard"
        assert question["type"] == "multiple"

        assert question["timer"] == 20

def test_check_answer_correct(socketio_client, mock_user, mock_quiz, mock_question):
    assert len(mock_user.completed_quizzes) == 0 # Ensure that the user has no completed quizzes

    mock_user.active_quiz = mock_quiz

    # Prepare data for the test
    data = {
        "email": mock_user.email,
        "question_id": mock_question.pk,
        "question_index": 1,
        "user_answer": "Test choice 1",  # Correct answer
        "time_left": 10,
        "max_time": 20,
    }

    # Emit the 'check_answer' event with the test data
    socketio_client.emit('check_answer', data)

    # # Wait for server response to ensure it's processed
    time.sleep(1)

    # Get the emitted events
    received = socketio_client.get_received()

    # Check if the correct event was emitted (answer_checked)
    answer_checked_event = next(
        (event for event in received if event["name"] == "answer_checked"), None
    )
    assert answer_checked_event is not None
    assert answer_checked_event["args"][0]["correct_answer"] == "Test choice 1"
    assert answer_checked_event["args"][0]["question_index"] == 1

    # Check if the quiz score was updated
    mock_quiz.save.assert_called_once()  # Ensure that the save method was called on the quiz

    # Check if the answered questions list is updated
    assert len(mock_quiz.answered_questions) == 1
    answered_question = mock_quiz.answered_questions[0]
    assert answered_question.question.pk == mock_question.pk
    assert answered_question.user_answer == "Test choice 1"

    # Verify that the quiz score was updated correctly (score > 0)
    assert mock_quiz.score == 5
    
    # Check if the quiz is completed
    if len(mock_quiz.answered_questions) == mock_quiz.total_questions:
        quiz_completed_event = next(
            (event for event in received if event["name"] == "quiz_completed"), None
        )
        assert quiz_completed_event is not None
        assert quiz_completed_event["args"][0]["score"] == mock_quiz.score
    
    assert len(mock_user.completed_quizzes) == 1 # Ensure that the user has 1 completed quiz

    

def test_check_answer_incorrect(socketio_client, mock_user, mock_quiz, mock_question):
    assert len(mock_user.completed_quizzes) == 0 # Ensure that the user has no completed quizzes

    mock_user.active_quiz = mock_quiz

    # Prepare data for the test
    data = {
        "email": mock_user.email,
        "question_id": mock_question.pk,
        "question_index": 1,
        "user_answer": "Test choice 2",  # Incorrect answer
        "time_left": 10,
        "max_time": 20,
    }

    # Emit the 'check_answer' event with the test data
    socketio_client.emit('check_answer', data)

    # # Wait for server response to ensure it's processed
    time.sleep(1)

    # Get the emitted events
    received = socketio_client.get_received()

    # Check if the correct event was emitted (answer_checked)
    answer_checked_event = next(
        (event for event in received if event["name"] == "answer_checked"), None
    )
    assert answer_checked_event is not None
    assert answer_checked_event["args"][0]["correct_answer"] == "Test choice 1"
    assert answer_checked_event["args"][0]["question_index"] == 1

    # Check if the quiz score was updated
    mock_quiz.save.assert_called_once()  # Ensure that the save method was called on the quiz

    # Check if the answered questions list is updated
    assert len(mock_quiz.answered_questions) == 1
    answered_question = mock_quiz.answered_questions[0]
    assert answered_question.question.pk == mock_question.pk
    assert answered_question.user_answer == "Test choice 2"

    # Verify that the quiz score was not updated (score = 0)
    assert mock_quiz.score == 0

    # Check if the quiz is completed
    if len(mock_quiz.answered_questions) == mock_quiz.total_questions:
        quiz_completed_event = next(
            (event for event in received if event["name"] == "quiz_completed"), None
        )
        assert quiz_completed_event is not None
        assert quiz_completed_event["args"][0]["score"] == mock_quiz.score

    assert len(mock_user.completed_quizzes) == 1 # Ensure that the user has 1 completed quiz
    


