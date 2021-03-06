from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired('Please enter your first name.')])
    last_name = StringField('Last name', validators=[DataRequired('Please enter your last name.')])
    email = StringField('Email', validators=[DataRequired('Please enter your email address.'), Email('Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password.'), Length(min=6, message='Password must have at least 6 characters.')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Please enter your email address.'), Email('Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password.')])
    submit = SubmitField('Log in')

class DeviceForm(FlaskForm):
    name = StringField(validators=[DataRequired('Please enter a name.')])
    submit = SubmitField('Add')

class RoomForm(FlaskForm):
    name = StringField(validators=[DataRequired('Please enter a name.')])
    submit = SubmitField('Add')