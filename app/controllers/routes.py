
from .main import main
from .about import about
from .help import help
from .settings import settings
from .user import sign_up, create_user, sign_in, authenticate, sign_out, remove_account, home_user, show_user, get_user_qrcode
from .api.user import update_user
from .api.medication import create_medication, update_medication, remove_medication
from .api.contact import create_contact, update_contact, remove_contact
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
        rule = "/usuario/eliminar_cuenta",
        view_func = remove_account,
        methods=["POST"]
    )

    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>",
        view_func = home_user,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/usuario/visualizar/<uuid:user_id>",
        view_func = show_user,
        methods=["GET"]
    )
    
    app.add_url_rule(
        rule = "/usuario/actualizar",
        view_func = update_user,
        methods=["POST"]
    )

    app.add_url_rule(
        rule = "/usuario/<uuid:user_id>/qr",
        view_func = get_user_qrcode,
        methods=["GET"]
    )

    app.add_url_rule(
        rule = "/usuario/medicamento/crear",
        view_func = create_medication,
        methods=["POST"]
    )
    
    app.add_url_rule(
        rule = "/usuario/medicamento/actualizar",
        view_func = update_medication,
        methods=["POST"]
    )
    
    app.add_url_rule(
        rule = "/usuario/medicamento/borrar",
        view_func = remove_medication,
        methods=["POST"]
    )

    app.add_url_rule(
        rule = "/usuario/contacto/crear",
        view_func = create_contact,
        methods=["POST"]
    )
    
    app.add_url_rule(
        rule = "/usuario/contacto/actualizar",
        view_func = update_contact,
        methods=["POST"]
    )
    
    app.add_url_rule(
        rule = "/usuario/contacto/borrar",
        view_func = remove_contact,
        methods=["POST"]
    )

def set_error_handler_routes(app):
    app.register_error_handler(404, page_not_found)
