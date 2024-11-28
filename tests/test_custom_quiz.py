# Test cases for custom quiz routes
# Routes are in ./controllers/custom_quiz_controller.py
from models.user_model import User

def test_create_custom_quiz(authenticated_client, mock_user):
    assert len(mock_user.created_quizzes) == 0 # Check that the user has no created quizzes

    # Create a custom quiz
    quiz_data = {
        "title": "Test Custom Quiz",
        "questions": [
            {
                "question": "What is the capital of France?",
                "correct_answer": "Paris",
                "incorrect_answers": ["London", "Berlin", "Madrid"],
                "category": "15",
                "type": "multiple",
                "difficulty": "easy"
            },
            {
                "question": "What is the capital of Spain?",
                "correct_answer": "Madrid",
                "incorrect_answers": ["Paris", "Berlin", "London"],
                "category": "15",
                "type": "multiple",
                "difficulty": "easy"
            }
        ]
    }

    response = authenticated_client.post("/custom-quiz", json=quiz_data)
    data = response.get_json()
    
    # Assert that the response is successful
    assert response.status_code == 200
    assert len(data) == 2 # Check that the response contains the correct number of questions
    assert len(mock_user.created_quizzes) == 1 # Check that the quiz was added to the user's created quizzes

def test_get_custom_quizzes(client, mock_user_created_quizzes):
    # register and login as a different user to test that
    # all users' custom quizzes are returned
    register_data = {
        "username": "test_user 2",
        "email": "test2@test2.com",
        "password": "password123"
    }

    response = client.post(
        "/register",
        json=register_data
    )

    assert response.status_code == 201
    assert response.json["message"] == "User created successfully."

    login_data = {
        "email": "test2@test2.com",
        "password": "password123"
    }

    response = client.post(
        "/login",
        json=login_data
    )

    assert response.status_code == 200
    assert response.json["message"] == "Login successful."

    quiz = {
        "title": "Test Custom Quiz 3",
        "questions": [
            {
                "question": "What is the capital of France?",
                "correct_answer": "Paris",
                "incorrect_answers": ["London", "Berlin", "Madrid"],
                "category": "15",
                "type": "multiple",
                "difficulty": "easy"
            },
            {
                "question": "What is the capital of Spain?",
                "correct_answer": "Madrid",
                "incorrect_answers": ["Paris", "Berlin", "London"],
                "category": "15",
                "type": "multiple",
                "difficulty": "easy"
            }
        ]
    }

    response = client.post("/custom-quiz", json=quiz)

    assert response.status_code == 200
    assert len(User.objects(email="test2@test2.com").first().created_quizzes) == 1 # 1 custom quiz created
    assert len(response.get_json()) == 2 # 2 questions in the quiz

    response = client.get("/get-custom-quizzes")

    assert response.status_code == 200
    assert "quizzes" in response.json
    assert len(response.json["quizzes"]) == 3 # 3 custom quizzes in total, 1 by this user and 2 by the authenticated user in the fixture

def test_delete_custom_quiz(authenticated_client, mock_user_created_quizzes):
    assert len(User.objects(email="test@test.com").first().created_quizzes) == 2 # 2 custom quizzes by this user exist

    # get the id of the first custom quiz
    quiz_id = User.objects(email="test@test.com").first().created_quizzes[0].id

    # delete the first custom quiz
    response = authenticated_client.delete("/delete-custom-quiz", json={"quiz_id": str(quiz_id)})

    assert response.status_code == 200
    assert response.json["message"] == "Quiz deleted"

    assert len(User.objects(email="test@test.com").first().created_quizzes) == 1 # 1 custom quiz left

def test_edit_custom_quiz(authenticated_client, mock_user_created_quizzes):
    assert User.objects(email="test@test.com").first().created_quizzes[0].title == "Test Custom Quiz 1" # Check the title of the first custom quiz
    
    # get the id of the first custom quiz
    quiz_id = User.objects(email="test@test.com").first().created_quizzes[0].id

    # edit the title of the first custom quiz
    response = authenticated_client.put("/edit-custom-quiz", json={"quiz_id": str(quiz_id), "title": "Edited Custom Quiz 1"})

    assert response.status_code == 200
    assert response.json["message"] == "Quiz updated"

    assert User.objects(email="test@test.com").first().created_quizzes[0].title == "Edited Custom Quiz 1" # Check that the title was updated

def test_begin_custom_quiz(authenticated_client, mock_user_created_quizzes):
    # get the id of the first custom quiz
    quiz_id = User.objects(email="test@test.com").first().created_quizzes[0].id

    # begin playing the first custom quiz
    response = authenticated_client.post("/begin-quiz", json={"quiz_id": str(quiz_id)})

    assert response.status_code == 200
    assert response.json["message"] == "Quiz started"

    # Check that the active quiz is now the first custom quiz
    assert User.objects(email="test@test.com").first().active_quiz.id == User.objects(email="test@test.com").first().created_quizzes[0].id