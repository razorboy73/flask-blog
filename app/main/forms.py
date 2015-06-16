__author__ = 'workhorse'
from ..models import Role, User
from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError



class NameForm(Form):
    name = StringField("What is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class EditProfileForm(Form):
    name = StringField("Real Name", validators=[Length(0,64)])
    location = StringField("Location", validators=[Length(0,64)])
    about_me = TextAreaField("About Me")
    submit = SubmitField("Submit")


class EditProfileAdminForm(Form):
    email = StringField("Email", validators=[DataRequired(), Length(1,64), Email()])
    username = StringField("Username", validators=[
        DataRequired(),
        Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
               'Usernames must only have letters,'
               'numbers, dots, or underscores')])
    confirmed = BooleanField("Confirmed")
    role = SelectField("Role", coerce=int)
    name = StringField("Real Name", validators=[Length(0,64)])
    location = StringField("Location", validators=[Length(0,64)])
    about_me = TextAreaField("About me")
    submit = SubmitField("Submit")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm,self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email= field.data).first():
            raise ValidationError("Email already registered")

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username = field.data).first():
            raise ValidationError("Username already registered")


class PostForm(Form):
    body = PageDownField("What is on your mind", validators=[DataRequired()])
    submit = SubmitField("Submit")