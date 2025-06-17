
from .main import main
from .about import about
from .help import help
from .settings import settings
from .user import sign_up, create_user, sign_in, authenticate, sign_out, show_user, edit_user, update_user, get_user_qrcode
from .error_handler import page_not_found

def set_routes(app):
    set_error_handler_routes(app)

    app.add_url_rule(
        rule = "/",
        view_func = main,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/ayuda",
        view_func = help,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/acerca",
        view_func = about,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/configuraciones",
        view_func = settings,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/usuario/registrar",
        view_func = sign_up,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/usuario/registrar",
        view_func = create_user,
        methods=["POST"]
    )

    app.add_url_rule(
        rule = "/usuario/iniciar_sesion",
        view_func = sign_in,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/usuario/iniciar_sesion",
        view_func = authenticate,
        methods=["POST"]
    )

    app.add_url_rule(
        rule = "/usuario/cerrar_sesion",
        view_func = sign_out,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>",
        view_func = show_user,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>/actualizar",
        view_func = edit_user,
        methods=["GET"]
    )
    
    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>/actualizar",
        view_func = update_user,
        methods=["POST"]
    )

    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>/qr",
        view_func = get_user_qrcode,
        methods=["GET"]
    )

def set_error_handler_routes(app):
    app.register_error_handler(404, page_not_found)
