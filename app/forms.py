from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed,FileRequired
from app import photos

class ImageSelectorForm(FlaskForm):
    image_used = RadioField( "Image Selection: ",choices=[('sample', 'Use the default Sample'), ("custom",'OR upload your own image')])
    photo_upload=FileField('Image (Leave empty in order to use the default sample)', validators=[FileAllowed(photos, 'Images only!')])
    message= TextAreaField("Message", validators=[DataRequired()])
    message_key=IntegerField("Key",validators=[DataRequired()])
    message_terminator= BooleanField("Use a message terminator")
    image_submit= SubmitField("Encode")

class ImageSelectorUploadForm(FlaskForm):
    photo_upload=FileField('Image', validators=[FileRequired(), FileAllowed(photos, 'Images only!')])
    message_key=IntegerField("Key",validators=[DataRequired()])
    image_submit= SubmitField("Decode")