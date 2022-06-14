from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

# app libraries
from app import db
from app.security import auth_required
from app.tokens import encode
from app.servers import servers

api = Blueprint("api", __name__)
user = Blueprint("user", __name__)

api.register_blueprint(user, url_prefix="/user")
api.register_blueprint(servers, url_prefix="/servers")


@api.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@user.route("/", methods=['POST'])
def login():
    data = request.get_json()
    if "email" not in data or "password" not in data:
        print(f"Login/signup attempt with missing email or password: {data}")
        return {"error": "Email and password are required"}, 400
    # first check if user exists
    email = data["email"]
    user_id = None
    user = db.get_user_by_email(email)
    if not user:
        print(f"User with email {email} not found. Creating new user.")
        # signup
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        new_user = {"email": email,
                    "password": hashed_password, "admin": False}
        user_id = db.insert_user(new_user)
    elif check_password_hash(user['password'], data["password"]):
        # login
        user_id = str(user.get("_id"))
    else:
        print(f"Invalid credentials login attempts: {data}")
        return {"error": "Ivalid email or password"}, 401
    return {"jwt": encode(user_id)}


@user.route("/", methods=['GET'])
@auth_required
def get_user(user):
    return user
