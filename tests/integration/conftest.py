import pytest
from unittest.mock import MagicMock
from models.user_model import User

@pytest.fixture(scope="session", autouse=True)
def set_testing_config():
    import os
    os.environ["TESTING"] = "1" # disables socketio message queue

@pytest.fixture
def app(set_testing_config):
    from app import create_app
    from mongoengine import connect, disconnect
    from mongomock import MongoClient

    # Set up the Flask app with mock database
    app = create_app()

    # Disconnect any existing database connections
    disconnect()

    # Connect to a local db for testing
    connect('QuizAppDB', mongo_client_class=MongoClient, uuidRepresentation="standard")

    # Yield the app for testing
    yield app

    # Disconnect the mock database after testing
    disconnect()

@pytest.fixture
def client(app):
    # Create a test client
    with app.test_client() as client:
        yield client

# Add a fixture to register and log in a test user for testing protected routes
@pytest.fixture
def authenticated_client(client):
    # Register and log in a test user
    register_data = {
        "email": "test@test.com",
        "username": "test_user",
        "password": "password123"
    }
    client.post("/register", json=register_data)
    
    login_data = {
        "email": "test@test.com",
        "password": "password123"
    }
    # login to be assigned jwt tokens as cookies
    login_response = client.post("/login", json=login_data)
    
    # Extract cookies from the login response
    cookies = login_response.headers.getlist("Set-Cookie")
    
    # Extract both access and refresh tokens
    access_token = login_response.json.get('access_token')
    refresh_token_cookie = next((cookie for cookie in cookies if "refresh_token" in cookie), None)
    
    # Assert that both cookies are set
    assert access_token, "Access token not issued"
    assert refresh_token_cookie, "Refresh token cookie not set"

    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

    return client

@pytest.fixture
def socketio_client(app, monkeypatch):
    # need this to stop threading in the quiz_controller while testing.
    monkeypatch.setenv('IS_TESTING', '1')

    from socket_manager import socketio

    # Create a test client for socket.io
    client = socketio.test_client(app, flask_test_client=app.test_client(), namespace='/singleplayer')
    yield client
    client.disconnect(namespace='/singleplayer')

@pytest.fixture
def mock_user(mocker):
    # Create a mock user object
    mock_user = MagicMock(spec=User)
    mock_user.pk = "user_id"
    mock_user.id = "user_id"
    mock_user.username = "test_user"
    mock_user.email = "test@test.com"
    mock_user.password = "password123"
    mock_user.completed_single_quizzes = []
    mock_user.completed_multi_quizzes = []
    mock_user.created_quizzes = []

    # Patch the User.objects.get method to return the mock user
    mocker.patch("models.user_model.User.objects", return_value=MagicMock(first=MagicMock(return_value=mock_user)))
    
    return mock_user

@pytest.fixture
def mock_question(mocker):
    from models.question_model import Question

    # Create a mock question object
    mock_question = MagicMock(spec=Question)
    mock_question.pk = "question_id"
    mock_question.prompt = "Test question"
    mock_question.category = "Test category"
    mock_question.difficulty = "Test difficulty"
    mock_question.type = "Test type"
    mock_question.correct_answer = "Test choice 1"
    mock_question.incorrect_answers = ["Test choice 2", "Test choice 3", "Test choice 4"]
    mock_question.timer = 10

    mocker.patch("models.question_model.Question.objects", return_value=MagicMock(first=MagicMock(return_value=mock_question)))

    return mock_question

@pytest.fixture
def mock_quiz(mocker, mock_user, mock_question):
    from models.quiz_model import Quiz
    
    # Create a mock quiz object
    mock_quiz = MagicMock(spec=Quiz)
    mock_quiz.id = "quiz_id"
    mock_quiz.title = "Test quiz"
    mock_quiz.score = 0
    mock_quiz.timestamp = "2021-01-01T00:00:00"
    mock_quiz.questions = [mock_question]
    mock_quiz.answered_questions = []
    mock_quiz.total_questions = 1
    mock_quiz.user_created = False
    mock_quiz.save = MagicMock()

    return mock_quiz

@pytest.fixture
def mock_user_history(mock_user, mock_quiz):
    mock_user.completed_single_quizzes = [mock_quiz, mock_quiz, mock_quiz, mock_quiz, mock_quiz, mock_quiz]

@pytest.fixture
def mock_user_creations(mock_user, mock_quiz):
    mock_user.created_quizzes = [mock_quiz, mock_quiz, mock_quiz]

# Fixture to create custom quizzes for testing
@pytest.fixture
def mock_user_created_quizzes(authenticated_client):
    quiz1 = {
        "title": "Test Custom Quiz 1",
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

    quiz2 = {
        "title": "Test Custom Quiz 2",
        "questions": [
            {
                "question": "What is the capital of Germany?",
                "correct_answer": "Berlin",
                "incorrect_answers": ["London", "Paris", "Madrid"],
                "category": "15",
                "type": "multiple",
                "difficulty": "easy"
            },
            {
                "question": "What is the capital of Italy?",
                "correct_answer": "Rome",
                "incorrect_answers": ["London", "Paris", "Madrid"],
                "category": "15",
                "type": "multiple",
                "difficulty": "easy"
            }
        ]
    }

    authenticated_client.post("/save-custom-quiz", json=quiz1)
    authenticated_client.post("/save-custom-quiz", json=quiz2)

    assert len(User.objects(email="test@test.com").first().created_quizzes) == 2
    
