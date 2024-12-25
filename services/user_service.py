# handles crud operations for user model

from models.user_model import User
from services.auth_service import hash_password, verify_password, create_jwt
from flask import make_response, jsonify
from datetime import datetime, timedelta, timezone
from enum import Enum

# enum for registration error handling
class RegisterUserResult(Enum):
    SUCCESS = "success"
    MISSING_FIELDS = "missing_fields"
    EMAIL_EXISTS = "email_exists"
    USERNAME_TOO_LONG = "username_too_long"
    PASSWORD_TOO_SHORT = "password_too_short"
    PASSWORD_TOO_LONG = "password_too_long"

# validate user input and create a new user
def register_user(username, email, password):

    if not username or not email or not password:
        return RegisterUserResult.MISSING_FIELDS
    
    # email must be unique
    if User.objects(email=email).first():
        return RegisterUserResult.EMAIL_EXISTS
    
    if len(username) > 20:
        return RegisterUserResult.USERNAME_TOO_LONG
    
    if len(password) < 8:
        return RegisterUserResult.PASSWORD_TOO_SHORT
    
    # bcrypt only supports inputs up to 72 bytes long
    # so limit to 70 to be safe.
    if len(password) > 70:
        return RegisterUserResult.PASSWORD_TOO_LONG

    new_user = User(username=username, email=email, password=hash_password(password))
    new_user.save()

    return RegisterUserResult.SUCCESS

# enum for login error handling
class LoginUserResult(Enum):
    SUCCESS = "success"
    MISSING_FIELDS = "missing_fields"
    INCORRECT_EMAIL_OR_PASSWORD = "incorrect_email_or_password"

# validate user input and log in the user by creating jwts
def login_user(email, password): 
    # generic error messages for security
    if not email or not password:
        return LoginUserResult.MISSING_FIELDS, None

    user = User.objects(email=email).first()

    # no user with that email
    if not user:
        return LoginUserResult.INCORRECT_EMAIL_OR_PASSWORD, None
    
    if not verify_password(password, user.password):
        return LoginUserResult.INCORRECT_EMAIL_OR_PASSWORD, None
    
    # on successful login, create jwts and return relevant user data
    access_token, refresh_token = create_jwt(user)
    
    data = {
        "email": user.email, 
        "username": user.username, 
        "access_token": access_token,
        "refresh_token": refresh_token
        }
    
    return LoginUserResult.SUCCESS, data

# refresh user's access token if their refresh token is still valid
def refresh_tokens(email, ref_exp):
    user = User.objects(email=email).first()

    # issue new access token if their refresh token is still valid
    access_token, refresh_token = create_jwt(user)

    data = {
        "email": user.email,
        "username": user.username,
        "access_token": access_token,
    }

    # if refresh token is close to expiring, issue a new one
    exp_datetime = datetime.fromtimestamp(ref_exp, tz=timezone.utc)
    current_datetime = datetime.now(timezone.utc)

    time_remaining = exp_datetime - current_datetime

    if time_remaining < timedelta(days=1):
        data["refresh_token"] = refresh_token
    
    return data

# get user's game play history
def get_user_history(id):
    user = User.objects(pk=id).first()
    return user.completed_quizzes

# get user's created quizzes
def get_user_creations(id):
    user = User.objects(pk=id).first()
    return user.created_quizzes

