from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from kiosk.models import User, Food
from kiosk.utils import log_func, entering, exiting
# from kiosk.utils import log_debug
# log_debug()

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),
        Email(),
        Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=8, max=64, message='Password length must be between %(min)d and %(max)d characters') ])
    confirm_password = PasswordField(
        label=('Confirm Password'),
        validators=[DataRequired(message='*Required'),
        EqualTo('password', message='Both password fields must be equal!')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

    @log_func(entering, exiting)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        else:
            excluded_chars = " ,*?!'^+%&/()=}][{$#/\\\""
            for char in username.data:
                if char in excluded_chars:
                    raise ValidationError(
                        f"Character {char} is not allowed in username.")

    @log_func(entering, exiting)
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    @log_func(entering, exiting)
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class MenuItemForm(FlaskForm):
    number = SelectField('Number', choices=[i for i in range(10)], default=1, coerce=int)
    foodname = HiddenField()
    submit = SubmitField('Submit')
