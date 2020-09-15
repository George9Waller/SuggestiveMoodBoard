from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from wtforms.fields.html5 import DateField

from models import User, Board


class NewBoard(FlaskForm):
    """Form for creating a board"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=1, max=30, message="Name must be max 30 characters")
        ]
    )

    venuesize = SelectField(
        'Venue Size',
        choices=['Small', 'Medium', 'Large'],
        validators=[
            DataRequired()
        ]
    )

    eventdate = DateField(
        'Event Date',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )


class DeleteBoardForm(FlaskForm):
    """Form for deleting a board with confirmation checkbox"""
    confirm = BooleanField('Confirm you want to delete this board', validators=[DataRequired()])


class IdeaForm(FlaskForm):
    """Form for editing or creating an idea"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=1, max=30, message="Name must be max 30 characters")
        ]
    )

    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(),
            Length(min=1, max=1000, message="Content cannot be over 1000 characters")
        ]
    )
