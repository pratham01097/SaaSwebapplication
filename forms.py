
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
##Creating a form for local login matching the database structure
class RegisterForm(FlaskForm):
    username=StringField(label="User Name")
    email_address=StringField(label="Email Address: ")
    password1=PasswordField(label="New password")
    password2=PasswordField(label="confirm your password")
    submit=SubmitField(label='submit')
