from flask import request, Blueprint
from services.auth_service import create_jwt, token_required, hash_password, verify_password
from models.user_model import User

users_bp = Blueprint('users_bp', __name__)

## TODO
## login route
## register route

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {"message": "Username, email and password are required."}, 401
    
    # email must be unique
    if User.objects(email=email).first():
        return {"message": "Email already registered."}, 401
    
    if len(password) < 8:
        return {"message": "Password must be at least 8 characters long."}, 401

    new_user = User(username=username, email=email, password=hash_password(password))
    new_user.save()

    return {"message": "User created successfully."}, 201


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
        access_token, refresh_token = create_jwt(user.username)
        return {"message": "Login successful.", "access_token": access_token, "refresh_token": refresh_token}, 200
    else:
        return {"message": "Incorrect email or password."}, 401

# @users_bp.route("/verify", methods=["POST"])
# def verify():
#     data = request.get_json()
#     entered_password = data.get('entered_password')
#     hashed_password = str.encode(data.get('hashed_password'))
#     return {"message": "Password is correct." if verify_password(entered_password, hashed_password) else "Password is incorrect."}, 200

# # testing token required decorator
# @users_bp.route("/protected", methods=["GET"])
# @token_required
# def protected_route(user_data):
#     return {"message": "This is a protected route.", "user_data": user_data}, 200