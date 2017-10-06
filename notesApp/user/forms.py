
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import PasswordField, StringField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User, Career, Role


class UserUpdateForm(FlaskForm):
    """
    Form for user to update their information
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])

    career = QuerySelectField(query_factory=lambda: Career.query.all(),
                               get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                               get_label="name")
    submit = SubmitField('Submit')

class NoteForm(FlaskForm):
    """
    Adding a note for a user
    """
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Note', validators=[DataRequired()])
    submit = SubmitField('Submit')