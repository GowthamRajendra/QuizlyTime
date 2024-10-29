import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import current_app as app, request

# create a JWT token for a user that has successfully logged in.
# keep user logged in 
def create_jwt(user):
    access_payload = {
        'sub': str(user.id),
        'email': user.email,
        "type": "access",  # this field will prevent refresh tokens from being used in place of access tokens
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=15) # expires in 15 minutes
    }

    refresh_payload = {
        'sub': str(user.id),
        'email': user.email,
        "type": "refresh",
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=7) # expires in 7 days
    }
    access_token = jwt.encode(access_payload, app.config["JWT_SECRET"], algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, app.config["JWT_SECRET"], algorithm="HS256")
    return access_token, refresh_token

# decorator to protected routes
def access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        
        if 'access_token' in request.cookies:
            access_token = request.cookies.get('access_token')
        
        if not access_token:
            return {'message': 'Access token is missing.'}, 401
        
        # Try to verify the access_token
        try:
            user_data = jwt.decode(access_token, app.config['JWT_SECRET'], algorithms=["HS256"])

            # prevent refresh tokens from being used in place of access tokens
            if user_data['type'] != 'access':
                return {'message': 'Access token is invalid.'}, 401
            
            return f(user_data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return {'message': 'Access token is expired.'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Access token is invalid.'}, 401
    
    return decorated

def refresh_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        refresh_token = None
        
        if 'refresh_token' in request.cookies:
            refresh_token = request.cookies.get('refresh_token')
        
        if not refresh_token:
            return {'message': 'Refresh token is missing.'}, 401
        
        # Try to verify the refresh_token
        try:
            user_data = jwt.decode(refresh_token, app.config['JWT_SECRET'], algorithms=["HS256"])

            # prevent access tokens from being used in place of refresh tokens
            if user_data['type'] != 'refresh':
                return {'message': 'Refresh token is invalid.'}, 401
            
            return f(user_data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return {'message': 'Refresh token is expired.'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Refresh token is invalid.'}, 401
    
    return decorated

# hash a newly registered user's password for safe storage in the db.
# salt isn't necessary to store because bcrypt stores it in the hashed password.
def hash_password(password):
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

# verify a user's entered password against the hashed password in the db.
def verify_password(entered_password, hashed_password):
    return bcrypt.checkpw(str.encode(entered_password), str.encode(hashed_password))

