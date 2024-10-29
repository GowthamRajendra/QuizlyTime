from flask import request, Blueprint, make_response, jsonify
from services.auth_service import create_jwt, access_token_required, refresh_token_required, hash_password, verify_password
from models.user_model import User


users_bp = Blueprint('users_bp', __name__)

# set CORS headers to allow json and cookies to be sent cross-origin
@users_bp.after_request
def cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {"message": "Username, email and password are required."}, 400
    
    # email must be unique
    if User.objects(email=email).first():
        return {"message": "Email already registered."}, 400
    
    if len(username) > 20:
        return {"message": "Username must be less than 20 characters long."}, 400
    
    if len(password) < 8:
        return {"message": "Password must be at least 8 characters long."}, 400
    
    # bcrypt only supports inputs up to 72 bytes long
    # so limit to 70 to be safe.
    if len(password) > 70:
        return {"message": "Password must be less than 70 characters long."}, 400

    new_user = User(username=username, email=email, password=hash_password(password))
    new_user.save()

    return {"message": "User created successfully."}, 201


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"message": "Missing email or password."}, 400

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
        response.headers.add('Set-Cookie', f'access_token={access_token}; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=10;')
        response.headers.add('Set-Cookie', f'refresh_token={refresh_token}; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=20;')
        
        return response
    else:
        return {"message": "Incorrect email or password."}, 401
    
# Refresh tokens if user is still logged in and the refresh token is still valid.
# Requested if the user did not log out the last time they visited the site.
# Requested if the user is currently using the site and the access token expires.
@users_bp.route("/auth/refresh", methods=["GET"])
@refresh_token_required
def refresh(user_data):
    # user_data from the refresh_token_required decorator
    user = User.objects(email=user_data.get('email')).first()

    # issue new access and refresh tokens if the previous refresh token is still valid
    access_token, refresh_token = create_jwt(user)

    response_data = {
            "message": "Login successful.", 
            "email": user.email, 
            "username": user.username, 
            }
    response = make_response(jsonify(response_data), 200)

    # set the tokens as httponly cookies guards against XSS attacks
    response.headers.add('Set-Cookie', f'access_token={access_token}; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=10;')
    response.headers.add('Set-Cookie', f'refresh_token={refresh_token}; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=20;')
    
    return response

@users_bp.route("/logout", methods=["POST"])
@access_token_required
def logout(_):
    response = make_response({"message": "Logout successful."}, 200)

    # delete the tokens by setting their max-age to 0
    response.headers.add('Set-Cookie', 'access_token=; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=0;')
    response.headers.add('Set-Cookie', 'refresh_token=; Secure; HttpOnly; SameSite=None; Path=/; Partitioned; Max-Age=0;')

    return response

# # testing token required decorator
@users_bp.route("/protected", methods=["GET"])
@access_token_required
def protected_route(user_data):
    return {"message": "This is a protected route.", "user_data": user_data}, 200