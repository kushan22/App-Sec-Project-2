from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class RegisterForm(FlaskForm):
    username = StringField('username', id="uname", validators=[DataRequired()])
    password = PasswordField('password', id="pword", validators=[DataRequired()])
    twoFactAuth = StringField('twoFactAuth', id="2fa")
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('username',id="uname", validators=[DataRequired()])
    password = PasswordField('password',id="pword", validators=[DataRequired()])
    twoFactAuth = StringField('twoFactAuth',id="2fa")
    submit = SubmitField('Login')

class SpellCheckerForm(FlaskForm):
    wordsToCheck = StringField('Words',id="inputtext", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Check')