
from wtforms.validators import Length

from app.forms import BaseForm
from app.forms.fields import OptionalStringField

class ContactForm(BaseForm):
    class Meta:
        csrf = False
    
    name = OptionalStringField(validators=[Length(max=64)])
    relation = OptionalStringField(validators=[Length(max=128)])
    address = OptionalStringField(validators=[Length(max=512)])
    phone = OptionalStringField(validators=[Length(max=20)])
