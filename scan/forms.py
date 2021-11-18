from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ScanForm(FlaskForm):
    text = TextAreaField('Input Ctrl-V + Ctrl-C result here', validators=[DataRequired()])
    submit = SubmitField('Scan me!')

