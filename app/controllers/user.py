
from flask import render_template, abort
from app.models import User

def sign_up():
    return render_template("create_user.html")

def create_user():
    pass

def sign_in():
    pass

def authenticate():
    pass

def sign_out():
    pass

def show_user(user_id):
    user = User.get(user_id)

    if not user:
        abort(404)
    
    return render_template("show_user.html", user=user)

def edit_user(user_id):
    pass

def update_user(user_id):
    pass
