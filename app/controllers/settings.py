
from flask import render_template

from app.session import get_authenticated_user

def settings():
    return render_template("settings.html", user=get_authenticated_user())
