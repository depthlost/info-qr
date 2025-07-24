
from flask import request
from werkzeug.datastructures import MultiDict

from app.controllers.api.utils.service import service
from app.controllers.api.utils.errors import *
from app.session import get_authenticated_user_id
from app.forms import MedicationForm
from app.models import Medication

@service
def create_medication():
    user_id = get_authenticated_user_id()

    if not user_id:
        raise UnauthorizedError()
    
    if not isinstance(request.json, dict) or \
        not isinstance(request.json.get("medication"), dict):
        raise BadRequestError()
    
    if Medication.get_count_by_user_id(user_id) >= 40:
        raise LimitError()

    form = MedicationForm(formdata=MultiDict(request.json["medication"]))

    if not form.validate():
        raise FormValidationError(errors=form.errors)
    
    medication = Medication(
        user_id=user_id,
        name=form.name.data,
        dosage=form.dosage.data,
        schedule=form.schedule.data,
    )
    
    medication.create()

    return {
        "message": "El medicamento fue creado con éxito.",
        "medication": medication.to_dict()
    }

@service
def update_medication():
    user_id = get_authenticated_user_id()

    if not user_id:
        raise UnauthorizedError()
    
    if not isinstance(request.json, dict) or \
        not isinstance(request.json.get("medication", {}).get("id"), int):
        raise BadRequestError()
    
    medication_data = request.json["medication"]
    medication = Medication.get(id=medication_data.pop("id"))

    if not medication or medication.user_id != user_id:
        raise NotFoundError()
    
    form = MedicationForm(formdata=MultiDict(request.json["medication"]))

    for field, field_name in [(form._fields.get(field_name), field_name) for field_name in medication_data.keys()]:
        if not field:
            raise BadRequestError(message=f"El campo '{field_name}' no existe.")

        field.validate(form)

    if form.errors:
        raise FormValidationError(errors=form.errors)
    
    medication.update(**{field_name: form.data[field_name] for field_name in medication_data.keys()})

    return {
        "message": "El medicamento fue modificado con éxito.",
        "medication": medication.to_dict()
    }

@service
def remove_medication():
    user_id = get_authenticated_user_id()

    if not user_id:
        raise UnauthorizedError()
    
    if not isinstance(request.json, dict) or \
        not isinstance(request.json.get("medication", {}).get("id"), int):
        raise BadRequestError()
    
    medication = Medication.get(id=request.json["medication"]["id"])

    if not medication or medication.user_id != user_id:
        raise NotFoundError()
    
    medication.remove()

    return { "message": "El medicamento fue eliminado con éxito." }
