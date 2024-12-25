import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import current_app as app, request
from enum import Enum

# create a JWT token for a user that has successfully logged in.
# keep user logged in 
def create_jwt(user):
    access_payload = {
        'sub': str(user.id),
        'email': user.email,
        "type": "access",  # this field will prevent refresh tokens from being used in place of access tokens
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=15)
    }

    refresh_payload = {
        'sub': str(user.id),
        'email': user.email,
        "type": "refresh",
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=14)
    }
    access_token = jwt.encode(access_payload, app.config["JWT_SECRET"], algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, app.config["JWT_SECRET"], algorithm="HS256")
    return access_token, refresh_token

# enum for validate token errors
class ValidateTokenResult(Enum):
    SUCCESS = "success"
    MISSING = "missing"
    INVALID = "invalid"
    EXPIRED = "expired"

# validate a user's jwt token
# seperated from token_required decorator for easier testing
def validate_token(token, token_type):
    if not token:
        return ValidateTokenResult.MISSING, None
    
    try:
        user_data = jwt.decode(token, app.config['JWT_SECRET'], algorithms=["HS256"])
        
        if user_data['type'] != token_type:
            return ValidateTokenResult.INVALID, None
        
        return ValidateTokenResult.SUCCESS, user_data

    except jwt.ExpiredSignatureError:
        return ValidateTokenResult.EXPIRED, None
    except jwt.InvalidTokenError:
        return ValidateTokenResult.INVALID, None
        


# decorator for protecting routes that require a user to have jwt access or refresh token
def token_required(token_type):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if f'{token_type}_token' in request.cookies:
                token = request.cookies.get(f'{token_type}_token')
            
            result, user_data = validate_token(token, token_type)

            match result:
                case ValidateTokenResult.SUCCESS:
                    return f(user_data, *args, **kwargs)
                case ValidateTokenResult.MISSING:
                    return {'message': f'{token_type} token is missing.'}, 401
                case ValidateTokenResult.INVALID:
                    return {'message': f'{token_type} token is invalid.'}, 401
                case ValidateTokenResult.EXPIRED:
                    return {'message': f'{token_type} token is expired.'}, 401 

        return decorated
    return decorator

# hash a newly registered user's password for safe storage in the db.
# salt isn't necessary to store because bcrypt stores it in the hashed password.
def hash_password(password):
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

# verify a user's entered password against the hashed password in the db.
def verify_password(entered_password, hashed_password):
    return bcrypt.checkpw(str.encode(entered_password), str.encode(hashed_password))

