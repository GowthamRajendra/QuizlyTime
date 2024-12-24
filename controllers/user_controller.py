from flask import request, Blueprint, make_response, jsonify
from datetime import datetime, timedelta, timezone
import os
from services.auth_service import create_jwt, access_token_required, refresh_token_required, hash_password, verify_password

from models.user_model import User
from services.user_service import register_user, RegisterUserResult

users_bp = Blueprint('users_bp', __name__)

# set CORS headers to allow json and cookies to be sent cross-origin
@users_bp.after_request
def cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = os.getenv("FRONT_END_URL", 'http://localhost:5173')
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    result = register_user(username=username, email=email, password=password)

    match result:
        case RegisterUserResult.SUCCESS:
            return {"message": "User created successfully."}, 201
        case RegisterUserResult.MISSING_FIELDS:
            return {"message": "Username, Email and Password are required."}, 400
        case RegisterUserResult.EMAIL_EXISTS:
            return {"message": "Email already registered."}, 403
        case RegisterUserResult.USERNAME_TOO_LONG:
            return {"message": "Username must be less than 20 characters long."}, 401
        case RegisterUserResult.PASSWORD_TOO_SHORT:
            return {"message": "Password must be at least 8 characters long."}, 401
        case RegisterUserResult.PASSWORD_TOO_LONG:
            return {"message": "Password must be less than 70 characters long."}, 401


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"message": "Incorrect email or password."}, 401

    user = User.objects(email=email).first()

    # no user with that email
    if not user:
        return {"message": "Incorrect email or password."}, 401

    if verify_password(password, user.password):
        access_token, refresh_token = create_jwt(user)
    
        response_data = {
            "message": "Login successful.", 
            "email": user.email, 
            "username": user.username, 
            }
        response = make_response(jsonify(response_data), 200)

        # set the tokens as httponly cookies guards against XSS attacks
        response.headers.add('Set-Cookie', f'access_token={access_token}; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=900;')
        response.headers.add('Set-Cookie', f'refresh_token={refresh_token}; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=1209600;')
        
        return response
    else:
        return {"message": "Incorrect email or password."}, 401
    
# Refresh access token if user is still logged in and the refresh token is still valid.
# Requested if the user did not log out the last time they visited the site.
# Requested if the user is currently using the site and the access token expires.
@users_bp.route("/auth/refresh", methods=["GET"])
@refresh_token_required
def refresh(user_data):
    # user_data from the refresh_token_required decorator
    user = User.objects(email=user_data.get('email')).first()

    # issue new access token if their refresh token is still valid
    access_token, refresh_token = create_jwt(user)

    response_data = {
            "message": "Refresh successful.", 
            "email": user.email, 
            "username": user.username, 
            }
    response = make_response(jsonify(response_data), 200)

    # if refresh token is close to expiring, issue a new one
    exp_datetime = datetime.fromtimestamp(user_data.get('exp'), tz=timezone.utc)
    current_datetime = datetime.now(timezone.utc)

    time_remaining = exp_datetime - current_datetime

    if time_remaining < timedelta(days=1):
        response.headers.add('Set-Cookie', f'refresh_token={refresh_token}; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=1209600;')

    # set the tokens as httponly cookies guards against XSS attacks
    response.headers.add('Set-Cookie', f'access_token={access_token}; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=900;')

    return response

@users_bp.route("/logout", methods=["POST"])
@access_token_required
def logout(_):
    response = make_response({"message": "Logout successful."}, 200)

    # delete the tokens by setting their max-age to 0
    response.headers.add('Set-Cookie', 'access_token=; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=0;')
    response.headers.add('Set-Cookie', 'refresh_token=; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=0;')

    return response


# format quizzes for profile page history/creations and quiz selection page
def format_quizzes(quizzes):
    results = [
        {
            "id": str(quiz.id),
            "title": quiz.title,
            "score": quiz.score,
            "timestamp": quiz.timestamp,
            "total_questions": quiz.total_questions
        } for quiz in quizzes
    ]

    response_data = {
        "quizzes": results
    }

    return response_data

# get previously played quizzes for profile page
@users_bp.route("/profile/history", methods=["GET"])
@access_token_required
def get_history(user_data):
    user = User.objects(pk=user_data['sub']).first()
    quizzes = user.completed_quizzes

    return make_response(jsonify(format_quizzes(quizzes)), 200)

# get quizzes that this user has created
@users_bp.route("/profile/creations", methods=["GET"])
@access_token_required
def get_creations(user_data):
    user = User.objects(pk=user_data['sub']).first()
    quizzes = user.created_quizzes

    return make_response(jsonify(format_quizzes(quizzes)), 200)
