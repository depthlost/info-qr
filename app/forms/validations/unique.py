
from wtforms.validators import ValidationError

class Unique():
    def __init__(self, class_, query_filter, message=None):
        self._message = message or 'El valor "{}" se encuentra en uso.'
        self._class = class_
        self._query_filter = query_filter

    def __call__(self, form, field):
        object_db = self.get_object_db(field.data)

        if object_db and object_db != form.model_object:
            raise ValidationError(self._message.format(field.data))

    def get_object_db(self, field_value):
        return self._class.query.filter_by(**{self._query_filter: field_value}).first()
