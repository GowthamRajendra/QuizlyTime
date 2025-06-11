from typing import List
from flask import request, Blueprint, make_response, jsonify
import os
from models.user_model import User
from services.auth_service import token_required

from services.user_service import register_user, RegisterUserResult, login_user, LoginUserResult, refresh_tokens, get_user_history, get_user_creations
from models.quiz_model import Quiz
from models.multiplayer_quiz_model import MultiplayerQuiz
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

    result, data = login_user(email=email, password=password)

    match result:
        # on successful login, return the user's email and username 
        # and set the access and refresh tokens as httpOnly cookies
        case LoginUserResult.SUCCESS:
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')

            # send the access token to the front end.
            response_data = {
                "message": "Login successful.",
                "email": data.get('email'),
                "username": data.get('username'),
                "access_token": access_token
            }
            response = make_response(jsonify(response_data), 200)

            # set refresh token as httponly to prevent xss, token is alive for 14 days
            response.set_cookie(key='refresh_token', value=refresh_token, path='/auth/refresh', max_age=60*60*24*14, secure=True, httponly=True, samesite="None")
            
            return response
        case LoginUserResult.MISSING_FIELDS:
            return {"message": "Email and Password are required."}, 400
        case LoginUserResult.INCORRECT_EMAIL_OR_PASSWORD:
            return {"message": "Incorrect email or password."}, 401
    
# Refresh access token if user is still logged in and the refresh token is still valid.
# Requested if the user did not log out the last time they visited the site.
# Requested if the user is currently using the site and the access token expires.
@users_bp.route("/auth/refresh", methods=["GET"])
@token_required("refresh")
def refresh(user_data):
    # user's email and refresh token expiration time
    email = user_data.get('email')
    ref_exp = user_data.get('exp')
    
    data = refresh_tokens(email, ref_exp)

    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    
    response_data = {
        "message": "Refresh successful.", 
        "email": data.get('email'), 
        "username": data.get('username'),
        "access_token": access_token 
    }

    response = make_response(jsonify(response_data), 200)

    # if refresh token is close to expiration, a new one will be issued.
    # httponly to prevent xss
    if refresh_token:
        response.set_cookie(key='refresh_token', value=refresh_token, path='/auth/refresh', max_age=60*60*24*14, secure=True, httponly=True, samesite="None")
    return response

@users_bp.route("/logout", methods=["POST"])
@token_required("access")
def logout(_):
    response = make_response({"message": "Logout successful."}, 200)

    # delete the refresh token by setting their max-age to 0
    # access token deletion is handled on the front-end
    response.set_cookie(key='refresh_token', value='', max_age=0, path='/auth/refresh')
    return response


# format quizzes for profile page history/creations and quiz selection page
def format_quizzes(quizzes: List[Quiz | MultiplayerQuiz], user_id):
    print("HISTORY USERID", user_id)
    results = [
        # Need to structure Singleplayer and Multiplayer quiz data differently
        {
            "title": quiz.title,
            "score": quiz.score,
            "timestamp": quiz.timestamp,
            "total_questions": quiz.total_questions,

        } if isinstance(quiz, Quiz) else {
            "title": quiz.title,
            "timestamp": quiz.timestamp,
            "is_multiplayer": True,
            "total_questions": quiz.total_questions,
            "score": quiz.getParticipant(user_id).score
        }
        for quiz in quizzes
    ]

    response_data = {
        "quizzes": results
    }

    return response_data

# get previously played quizzes for profile page
@users_bp.route("/profile/history", methods=["GET"])
@token_required("access")
def get_history(user_data):
    id = user_data['sub']

    history = get_user_history(id)

    return make_response(jsonify(format_quizzes(history, id)), 200)

# get quizzes that this user has created
@users_bp.route("/profile/creations", methods=["GET"])
@token_required("access")
def get_creations(user_data):
    id = user_data['sub']
    
    creations = get_user_creations(id)

    return make_response(jsonify(format_quizzes(creations, id)), 200)
