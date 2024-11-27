
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
    
    assert response.status_code == 401
    assert response.json["message"] == "Username, email and password are required."

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
    
    assert response.status_code == 401
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
        "email": "test@test.com",
        "password": "password3"
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
