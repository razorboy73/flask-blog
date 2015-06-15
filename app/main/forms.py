__author__ = 'workhorse'
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length



class NameForm(Form):
    name = StringField("What is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class EditProfileForm(Form):
    name = StringField("Real Name", validators=[Length(0,64)])
    location = StringField("Location", validators=[Length(0,64)])
    about_me = TextAreaField("About Me")
    submit = SubmitField("Submit")