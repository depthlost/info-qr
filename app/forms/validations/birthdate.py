
import datetime
from wtforms.validators import ValidationError

class Birthdate():
    def __call__(self, form, field):
        if not field.data:
            return
        elif field.data < datetime.date(1900, 1, 1):
            raise ValidationError("La fecha de nacimiento no puede ser menor al año 1900.")
        elif field.data > datetime.date.today():
            raise ValidationError("La fecha de nacimiento no puede ser mayor a hoy.")
