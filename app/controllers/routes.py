
from .main import main
from .about import about
from .help import help
from .settings import settings
from .user import new_user, create_user, show_user, request_edit_user, edit_user, update_user

def set_routes(app):
    app.add_url_rule(
        rule = "/",
        view_func = main
    )
    app.add_url_rule(
        rule = "/ayuda",
        view_func = help
    )
    app.add_url_rule(
        rule = "/nosotros",
        view_func = about
    )
    app.add_url_rule(
        rule = "/configuraciones",
        view_func = settings
    )
    app.add_url_rule(
        rule = "/usuario/registrar",
        view_func = new_user
    )
    app.add_url_rule(
        rule = "/usuario/crear",
        view_func = create_user,
        methods=["POST"]
    )
    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>",
        view_func = show_user
    )
    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>/solicitar_editar",
        view_func = request_edit_user,
        methods=["POST"]
    )
    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>/editar",
        view_func = edit_user
    )
    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>/actualizar",
        view_func = update_user,
        methods=["POST"]
    )