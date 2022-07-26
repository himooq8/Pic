from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, FileField
from wtforms.validators import DataRequired, EqualTo, Length

# -- Create Form Class's Here --
# -- Login Form --
class PhotoForm(FlaskForm):
    number = StringField("Enter Number Here", validators=[DataRequired()])
    picture = FileField("Upload Here", validators=[DataRequired()])
    submit = SubmitField("Submit")

# -- Search Form --
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")

