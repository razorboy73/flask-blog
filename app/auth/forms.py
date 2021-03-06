__author__ = 'workhorse'
from flask.ext.wtf import Form
from wtforms import ValidationError, StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..models import User

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField("log in")


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(),Length(1,64), Email()])
    username = StringField("Username", validators=[
        DataRequired(),
        Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
               'Usernames must only have letters,'
               'numbers, dots, or underscores')])

    password = PasswordField("Password", validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("Email or password is already in use")

    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("Username is already in use")

class ChangePasswordForm(Form):
    old_password = PasswordField("Old Passowrd", validators=[DataRequired()])
    password = PasswordField("New Password", validators=[DataRequired(),
                    EqualTo('password2', message="Passwords must match")])
    password2=PasswordField("Confirm new password", validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField("New Password", validators=[DataRequired(), EqualTo('password2', message="Passwords must match")])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first() is None:
            raise ValidationError("Unknown email address")

