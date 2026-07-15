from flask_wtf import FlaskForm
from wtforms import  StringField, TextAreaField, SubmitField

from wtforms.validators import DataRequired,length

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(min=1, max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), length(min=1, max=1000)])
    submit = SubmitField('Save Notess')