
import uuid
from flask import session
from app.models import User

def user_is_authenticated():
    return "user_id" in session

def get_authenticated_user_id():
    user_id = session.get("user_id", None)

    if not user_id:
        return None
    
    return uuid.UUID(hex=user_id)

def get_authenticated_user():
    user_id = session.get("user_id", None)

    if not user_id:
        return None
    
    return User.get(uuid.UUID(hex=user_id))

def login_user(user):
    session["user_id"] = user.id.hex

def logout_user():
    session.pop("user_id", None)
