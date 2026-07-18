from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import PasswordField

from wtforms.validators import EqualTo, Length

class PasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )

    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')]
    )

    submit = SubmitField("Change Password")
class ProfileForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField("Update Profile")