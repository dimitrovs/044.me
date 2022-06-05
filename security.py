from functools import wraps
from flask import abort, request

# app libraries
import db
from tokens import decode


def get_token(header: str):
    if not header or not header.startswith("Bearer "):
        return None
    else:
        return header.split("Bearer ")[1]


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = get_token(request.headers.get("Authorization"))

        if not token:
            print("Received request without valid token.")
            abort(401)

        try:
            data = {}
            data = decode(token)
            current_user = db.get_user_by_id(data.get("id"))
            del current_user["password"]
            current_user["_id"] = str(current_user["_id"])
        except Exception as e:
            print(f"Failed to verify token: {token} decoded as {data}")
            print(e)
            abort(401)

        return f(current_user, *args, **kwargs)
    return decorator
