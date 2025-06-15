
from app.forms import BaseForm
from app.models import User

from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from app.forms.validations.unique import Unique

class SignUpForm(BaseForm):
    name = StringField(validators=[DataRequired(), Length(max=64)])
    surname = StringField(validators=[DataRequired(), Length(max=64)])
    email = EmailField(validators=[DataRequired(), Unique(User, "email"), Email(), Length(max=128)])
    password = PasswordField(validators=[DataRequired(), Length(max=128)])
    