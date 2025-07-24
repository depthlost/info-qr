
from wtforms.validators import Length

from app.forms import BaseForm
from app.forms.fields import OptionalStringField


class MedicationForm(BaseForm):
    class Meta:
        csrf = False
    
    name = OptionalStringField(validators=[Length(max=128)])
    dosage = OptionalStringField(validators=[Length(max=1024)])
    schedule = OptionalStringField(validators=[Length(max=1024)])
