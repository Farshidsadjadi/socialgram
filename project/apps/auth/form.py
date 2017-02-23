from wtforms import Form, StringField, PasswordField, validators, IntegerField
from models import User

class RegistrationForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.required(), validators.Email()])
    phone = IntegerField('Phone Number')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    firstname = StringField('First Name', [validators.Length(min=4, max=25), validators.required()])
    lastname = StringField('Last Name', [validators.Length(min=3, max=35), validators.required()])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.required(), validators.Email()])
    password = PasswordField('Password')

    def validate_email(form, field):
        if User.userexist(field.data) == False:
            raise validators.ValidationError("User Not Exist!")

    def validate_password(form, field):
        user = User.userexist(form.email.data)
        if user and user.pass_match(field.data) == False:
            raise validators.ValidationError("Password Not Match!")