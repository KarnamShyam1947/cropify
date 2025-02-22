import email
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import EqualTo

def my_required_field(form, field):
    if field.data == "":
        raise ValidationError('this filed is required')

class LoginForm(FlaskForm):
    username = StringField("Email", validators=[my_required_field])
    password = PasswordField("Password", validators=[my_required_field])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[my_required_field])
    username = StringField("Username", validators=[my_required_field])
    password = PasswordField("Password", validators=[my_required_field])
    password1 = PasswordField("Reenter Password", validators=[EqualTo("password", "password and conform password must match"), my_required_field])
    submit = SubmitField("Register")

class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[my_required_field])
    submit = SubmitField("submit")

class SetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[my_required_field])
    password1 = PasswordField("Reenter Password", validators=[EqualTo("password", "password and conform password must match"), my_required_field])
    submit = SubmitField("submit")
