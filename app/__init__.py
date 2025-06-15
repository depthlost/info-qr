
import locale
from flask import Flask

from app.config import Config
from app.controllers import routes
from app import database
from app.session import user_is_authenticated, get_authenticated_user_id


def create_app():
    locale.setlocale(locale.LC_ALL, ("es_AR", "UTF-8"))

    app = Flask(__name__)
    app.config.from_object(Config.get())
    
    routes.set_routes(app)
    database.set_database(app)

    app.jinja_env.globals.update(user_is_authenticated=user_is_authenticated)
    app.jinja_env.globals.update(get_authenticated_user_id=get_authenticated_user_id)

    return app
