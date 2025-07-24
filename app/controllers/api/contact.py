
from flask import request
from werkzeug.datastructures import MultiDict

from app.controllers.api.utils.service import service
from app.controllers.api.utils.errors import *
from app.session import get_authenticated_user
from app.forms import ContactForm
from app.models import Contact

@service
def create_contact():
    user = get_authenticated_user()

    if not user:
        raise UnauthorizedError()
    
    if not isinstance(request.json, dict) or \
        not isinstance(request.json.get("contact"), dict) or \
        not request.json.get("type") in ("support_persons", "other_professionals"):
        raise BadRequestError()
    
    if (request.json["type"] == "support_persons" and len(user.support_persons) >= 20) or \
        (request.json["type"] == "other_professionals" and len(user.other_professionals) >= 20):
        raise LimitError()

    form = ContactForm(formdata=MultiDict(request.json["contact"]))

    if not form.validate():
        raise FormValidationError(errors=form.errors)
        
    contact = Contact(
        name=form.name.data,
        relation=form.relation.data,
        address=form.address.data,
        phone=form.phone.data,
        supported_user=user if request.json["type"] == "support_persons" else None,
        professional_user=user if request.json["type"] == "other_professionals" else None
    )

    contact.create()

    return {
        "message": "El contacto fue creado con éxito.",
        "contact": contact.to_dict()
    }

@service
def update_contact():
    user = get_authenticated_user()

    if not user:
        raise UnauthorizedError()
    
    if not isinstance(request.json, dict) or \
        not isinstance(request.json.get("contact", {}).get("id"), int):
        raise BadRequestError()
    
    contact_data = request.json["contact"]
    contact = user.get_contact_by_id(contact_id=contact_data.pop("id"))

    if not contact:
        raise NotFoundError()
    
    form = ContactForm(formdata=MultiDict(contact_data))

    for field, field_name in [(form._fields.get(field_name), field_name) for field_name in contact_data.keys()]:
        if not field:
            raise BadRequestError(message=f"El campo '{field_name}' no existe.")

        field.validate(form)

    if form.errors:
        raise FormValidationError(errors=form.errors)

    contact.update(**{field_name: form.data[field_name] for field_name in contact_data.keys()})

    return {
        "message": "El contacto fue modificado con éxito.",
        "contact": contact.to_dict()
    }

@service
def remove_contact():
    user = get_authenticated_user()

    if not user:
        raise UnauthorizedError()

    if not isinstance(request.json, dict) or \
        not isinstance(request.json.get("contact", {}).get("id"), int):
        raise BadRequestError()
    
    contact = user.get_contact_by_id(
        contact_id=request.json["contact"]["id"],
        contact_type=("support_persons", "other_professionals")
    )

    if not contact:
        raise NotFoundError()
    
    contact.remove()

    return { "message": "El contacto fue eliminado con éxito." }
