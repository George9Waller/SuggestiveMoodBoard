from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo

from models import User
from StaticLookupDictionaries import usertype_to_num


# custom validators to verify if the username or email is already in use
def name_exists(form, field):
    if User.select().where(User.UserName == field.data).exists():
        raise ValidationError('User with that username already exists!')


def email_exists(form, field):
    if User.select().where(User.Email == field.data).exists():
        raise ValidationError('User with that email already exists!')


def check_email_exists(form, field):
    if User.select().where(User.Email == field.data).exists():
        return
    else:
        raise ValidationError('There is no account with that email')


class RegisterFrom(FlaskForm):
    """Form to register a new account"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]{1,20}$',
                   message="Username must only have letters, numbers, underscores, no spaces and be 20 or less "
                           "characters"),
            name_exists
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Email undeliverable", check_deliverability=True),
            email_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=20),
            Regexp('(?=^.{8,20}$)((?=.*\w)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[|!"$%&\/\[\]\(\)\?\^\'\\\+\-\*]))^.*',
                   message="Password must have: a digit, a lower-case character, an upper-case character, a special "
                           '''character |!"$%&/\()[]?^'+-* and be between 8 and 20 characters inclusive'''),
            EqualTo('password2', message="Passwords must match")
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
    usertype = SelectField(
        'User Type',
        choices=[*usertype_to_num],
        validators=[DataRequired()],
        render_kw={"placeholder": "Select User Type"}
    )


class LoginForm(FlaskForm):
    """Form to login"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RequestPasswordResetForm(FlaskForm):
    """Form to request a password reset email"""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Email undeliverable", check_deliverability=True),
            check_email_exists
        ]
    )


class ResetPasswordForm(FlaskForm):
    """Form to make a new password"""
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=20),
            Regexp('(?=^.{8,20}$)((?=.*\w)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[|!"$%&\/\[\]\(\)\?\^\'\\\+\-\*]))^.*',
                   message="Password must have: a digit, a lower-case character, an upper-case character, a special "
                           '''character |!"$%&/\()[]?^'+-* and be between 8 and 20 characters inclusive'''),
            EqualTo('password2', message="Passwords must match")
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
