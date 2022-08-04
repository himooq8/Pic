from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, FileField, MultipleFileField
from wtforms.validators import DataRequired, EqualTo, Length

# -- Create Form Class's Here --
# -- Login Form --
class PhotoForm(FlaskForm):
    number = StringField("Phone Number", validators=[DataRequired()], render_kw={"placeholder": "Customer Phone Number Here"})
    picture = MultipleFileField("Upload Here", validators=[DataRequired()])
    submit = SubmitField("Submit")

# -- Search Form --
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")

