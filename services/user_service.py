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
