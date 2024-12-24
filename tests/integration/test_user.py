# Test cases for user routes
# Routes are in ./controllers/user_controller.py

def test_register_user(client):
    data = {
        "username": "test_user",
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/register", 
        json=data
        )

    assert response.status_code == 201
    assert response.json["message"] == "User created successfully."

def test_register_user_missing_data(client):
    data = {
        "username": "test_user",
        "email": "",
        "password": "password123"
    }

    response = client.post(
        "/register", 
        json=data
        )
    
    assert response.status_code == 400
    assert response.json["message"] == "Username, Email and Password are required."

def test_register_user_existing_email(client):
    data = {
        "username": "test_user",
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/register", 
        json=data
        )
    
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully."

    response = client.post(
        "/register", 
        json=data
        )
    
    assert response.status_code == 403
    assert response.json["message"] == "Email already registered."

def test_register_user_long_username(client):
    data = {
        "username": "test_user_test_user_test_user",
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/register", 
        json=data
        )
    
    assert response.status_code == 401
    assert response.json["message"] == "Username must be less than 20 characters long."

def test_register_user_short_password(client):
    data = {
        "username": "test_user",
        "email": "test@test.com",
        "password": "pass"
    }

    response = client.post(
        "/register", 
        json=data
        )
    
    assert response.status_code == 401
    assert response.json["message"] == "Password must be at least 8 characters long."

def test_register_user_long_password(client):
    data = {
        "username": "test_user",
        "email": "test@test.com",
        "password": "passwordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpassword"
    }

    response = client.post(
        "/register", 
        json=data
        )
    
    assert response.status_code == 401
    assert response.json["message"] == "Password must be less than 70 characters long."

def test_login_user(client):
    register_data = {
        "username": "test_user",
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/register",
        json=register_data
    )

    assert response.status_code == 201
    assert response.json["message"] == "User created successfully."

    login_data = {
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/login",
        json=login_data
    )

    assert response.status_code == 200
    assert response.json["message"] == "Login successful."

def test_login_user_incorrect_email(client):
    register_data = {
        "username": "test_user",
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/register",
        json=register_data
    )

    assert response.status_code == 201
    assert response.json["message"] == "User created successfully."

    login_data = {
        "email": "test@test.co",
        "password": "password123"
    }

    response = client.post(
        "/login",
        json=login_data
    )

    assert response.status_code == 401
    assert response.json["message"] == "Incorrect email or password."

def test_login_user_missing_data(client):
    data = {
        "email": "",
        "password": "password123"
    }

    response = client.post(
        "/login", 
        json=data
        )
    
    assert response.status_code == 401
    assert response.json["message"] == "Incorrect email or password."

def test_login_user_not_existing(client):
    data = {
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/login", 
        json=data
        )
    
    assert response.status_code == 401
    assert response.json["message"] == "Incorrect email or password."

def test_login_user_incorrect_password(client):
    register_data = {
        "username": "test_user",
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/register",
        json=register_data
    )

    assert response.status_code == 201
    assert response.json["message"] == "User created successfully."

    login_data = {
        "email": "test@test.com",
        "password": "password1234"
    }

    response = client.post(
        "/login",
        json=login_data
    )

    assert response.status_code == 401
    assert response.json["message"] == "Incorrect email or password."

def test_logout_user(client):
    register_data = {
        "username": "test_user",
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/register",
        json=register_data
    )

    assert response.status_code == 201
    assert response.json["message"] == "User created successfully."

    login_data = {
        "email": "test@test.com",
        "password": "password123"
    }

    response = client.post(
        "/login",
        json=login_data
    )

    assert response.status_code == 200
    assert response.json["message"] == "Login successful."

    response = client.post(
        "/logout"
    )

    assert response.status_code == 200
    assert response.json["message"] == "Logout successful."

def test_get_history(authenticated_client, mock_user_history):
    response = authenticated_client.get("/profile/history")

    assert response.status_code == 200
    assert "quizzes" in response.json
    assert len(response.json["quizzes"]) == 6
    assert response.json.get("quizzes") == [
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1},
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1},
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1},
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1},
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1},
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1}
        ]

def test_get_creations(authenticated_client, mock_user_creations):
    response = authenticated_client.get("/profile/creations")

    assert response.status_code == 200
    assert "quizzes" in response.json
    assert len(response.json["quizzes"]) == 3
    assert response.json.get("quizzes") == [
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1},
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1},
        {"id": "quiz_id", "title": "Test quiz", "score": 0, "timestamp": "2021-01-01T00:00:00", "total_questions": 1},
        ]
