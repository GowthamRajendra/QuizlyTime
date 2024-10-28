import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import current_app as app, request

# create a JWT token for a user that has successfully logged in.
# keep user logged in 
def create_jwt(username):
    access_payload = {
        'sub': username,
        "type": "access",  # this field will prevent refresh tokens from being used in place of access tokens
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30) # expires in 30 minutes
    }

    refresh_payload = {
        "type": "refresh",
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=30) # expires in 30 days
    }
    access_token = jwt.encode(access_payload, app.config["JWT_SECRET"], algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, app.config["JWT_SECRET"], algorithm="HS256")
    return access_token, refresh_token

# decorator to protected routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # check if token exists
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
        
        if not token:
            return {'message': 'Token is missing.'}, 401
        
        # Try to verify the token
        try:
            user_data = jwt.decode(token, app.config['JWT_SECRET'], algorithms=["HS256"])

            # prevent refresh tokens from being used in place of access tokens
            if user_data['type'] != 'access':
                return {'message': 'Token is invalid.'}, 401
            
            return f(user_data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return {'message': 'Token is expired.'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token is invalid.'}, 401
    
    return decorated

# hash a newly registered user's password for safe storage in the db.
# salt isn't necessary to store because bcrypt stores it in the hashed password.
def hash_password(password):
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

# verify a user's entered password against the hashed password in the db.
def verify_password(entered_password, hashed_password):
    return bcrypt.checkpw(str.encode(entered_password), str.encode(hashed_password))

