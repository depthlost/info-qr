
from flask import request
from werkzeug.datastructures import MultiDict

from app.controllers.api.utils.service import service
from app.controllers.api.utils.errors import *
from app.session import get_authenticated_user_id
from app.forms import UserForm
from app.models import User

@service
def update_user():
    user_id = get_authenticated_user_id()

    if not user_id:
        raise UnauthorizedError()
    
    if not isinstance(request.json, dict) or \
        not isinstance(request.json.get("user"), dict):
        raise BadRequestError()

    user_data = request.json["user"]

    form = UserForm(formdata=MultiDict(user_data))

    for field, field_name in [(form._fields.get(field_name), field_name) for field_name in user_data.keys()]:
        if not field:
            raise BadRequestError(message=f"El campo '{field_name}' no existe.")

        field.validate(form)
    
    if form.errors:
        raise FormValidationError(errors=form.errors)

    was_modified = User.update_by_id(
        id=user_id,
        data={field_name: form.data[field_name] for field_name in user_data.keys()}
    )

    if not was_modified:
        raise NotFoundError(message="No existe la/el usuaria/o.")

    return { "message": "La modificación se realizó con éxito." }
