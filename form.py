from wtforms import Form, StringField, PasswordField, validators, IntegerField

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
