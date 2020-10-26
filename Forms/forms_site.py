from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, TextAreaField
from wtforms_components import ColorField
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


class DeleteIdeaForm(FlaskForm):
    """Form for deleting an idea with confirmation checkbox"""
    confirm = BooleanField('Confirm you want to delete this idea', validators=[DataRequired()])


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
            Length(min=0, max=1000, message="Content cannot be over 1000 characters")
        ]
    )

    """tags"""
    colour = ColorField(
        'Colour',
        validators=[]
    )

    fixturetype = SelectField(
        'Fixture Type',
        validators=[],
        choices=['', 'Fresnel', 'Profile', 'LED', 'Par', 'Mover-Wash', 'Mover-Beam', 'Mover-Spot', 'Special', 'Intelligent']
    )

    fixtureangle = SelectField(
        'Fixture Angle',
        validators=[],
        choices=['', 'Face', 'Back', 'Side', 'Top', 'Overhead', 'Foot', 'Special']
    )

    red = StringField(
        'Red',
        validators=[Length(max=20)]
    )
    green = StringField(
        'Green',
        validators=[Length(max=20)]
    )
    blue = StringField(
        'Blue',
        validators=[Length(max=20)]
    )
    yellow = StringField(
        'Yellow',
        validators=[Length(max=20)]
    )
