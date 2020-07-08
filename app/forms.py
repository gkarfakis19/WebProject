from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ImageSelectorForm(FlaskForm):
    message= StringField("Message", validators=[DataRequired()])
    message_key=IntegerField("Key",validators=[DataRequired()])
    message_terminator= BooleanField("Use a message terminator")
    image_submit= SubmitField("Encode")
