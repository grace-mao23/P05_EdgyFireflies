from flask_wtf import FlaskForm
from wtforms import Form,StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import widgets

class SearchForm(FlaskForm):
    search = StringField('Query:', validators=[Length(min=0, max=80)])
    submit = SubmitField('Search')
