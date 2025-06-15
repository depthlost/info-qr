
from app.forms import BaseForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class SignInForm(BaseForm):
    email = EmailField(validators=[DataRequired(), Email(), Length(max=128)])
    password = PasswordField(validators=[DataRequired()])
