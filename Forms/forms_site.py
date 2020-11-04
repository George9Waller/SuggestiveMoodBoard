from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SelectField, BooleanField, TextAreaField, FieldList, FormField, \
    SelectMultipleField
from wtforms_components import ColorField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from wtforms.fields.html5 import DateField

from models import User, Board, Tag


# From: https://stackoverflow.com/questions/14433104/how-can-i-disable-the-wtforms-selectfield-choices-validation
class NonValidatingSelectMultipleField(SelectMultipleField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """
    def pre_validate(self, form):
        pass


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


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
        'Project Size',
        choices=['Small', 'Medium', 'Large'],
        validators=[
            DataRequired()
        ]
    )

    eventdate = DateField(
        'Project Date',
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

    addtotag = NonValidatingSelectMultipleField(
        'Tag (select multiple by holding down control/command)'
    )


class AddTagForm(FlaskForm):
    """Form for creating a new tag"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(max=30, message="Name must be 30 characters or less")
        ]
    )

    colour = ColorField(
        'Colour',
        validators=[DataRequired()]
    )


class DeleteTagForm(FlaskForm):
    """Delete a tag from selection"""
    selectTag = NonValidatingSelectField(
        'Select Tag',
        choices=[],
        validators=[DataRequired(message="Must make a choice")],
        coerce=int
    )

    confirm = BooleanField('Confirm you want to delete this tag', validators=[DataRequired()])
