from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired, ValidationError


class EmailForm(FlaskForm):

    def validate_email(self, email):
        if '@gmail.com' not in email.data:
            raise ValidationError("Please, ensure you enter a google email account.")

    email = StringField(label='Email', validators=[Email(), Length(min=3), DataRequired()])
    password = PasswordField(label='Email Application Password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Submit')
