from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateField,
    TimeField,
    SubmitField
)
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description"
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low")
        ]
    )

    due_date = DateField(
        "Due Date",
        format="%Y-%m-%d"
    )

    due_time = TimeField(
        "Due Time",
        format="%H:%M"
    )

    submit = SubmitField("Save Task")