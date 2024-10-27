from flask import request, Blueprint
from services.auth_service import create_jwt, token_required, hash_password, verify_password

users_bp = Blueprint('users_bp', __name__)

## TODO
## login route
## register route

# placeholder login to test jwt creation
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    access_token, refresh_token = create_jwt(username)
    return {"access_token": access_token, "refresh_token": refresh_token}, 200

# placeholder routes to test password hashing
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return {"message": f"{username} registered successfully.", "hashed_password": hash_password(password).decode()}, 201

@users_bp.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    entered_password = data.get('entered_password')
    hashed_password = str.encode(data.get('hashed_password'))
    return {"message": "Password is correct." if verify_password(entered_password, hashed_password) else "Password is incorrect."}, 200

# testing token required decorator
@users_bp.route("/protected", methods=["GET"])
@token_required
def protected_route(user_data):
    return {"message": "This is a protected route.", "user_data": user_data}, 200