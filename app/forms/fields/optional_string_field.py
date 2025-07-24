
from wtforms import StringField
from wtforms.validators import Optional

class OptionalStringField(StringField):
    def __init__(self, *args, **kwargs):
        validators = kwargs.pop("validators", [])
        filters = kwargs.pop("filters", [])
        
        super().__init__(
            *args,
            validators=[Optional()] + validators,
            filters=[lambda input: input.strip() or None if isinstance(input, str) else input] + filters,
            **kwargs
        )
