
from flask import render_template, abort
from app.models import User

def new_user():
    return render_template("create_user.html")

def create_user():
    pass

def show_user(user_id):
    user = User.get(user_id)

    if not user:
        abort(404)
    
    return render_template("show_user.html", user=user)

def request_edit_user(user_id):
    pass

def edit_user(user_id):
    pass

def update_user(user_id):
    pass
