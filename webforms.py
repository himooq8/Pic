from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea

# -- Create Form Class's Here --
# -- Name Form --
class NamerForm(FlaskForm):
    name = StringField("Whats Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")
# -- Password Form --
class PasswordForm(FlaskForm):
    email = StringField("Whats Your Email?", validators=[DataRequired()])
    password_hash = PasswordField("Password")
    submit = SubmitField("Submit")
# -- User Form --
class UserForm(FlaskForm):
    name = StringField("", validators=[DataRequired()], render_kw={"placeholder": "Name"})
    username = StringField("", validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField("", validators=[DataRequired()], render_kw={"placeholder": "Email"})
    favorite_color = StringField("", render_kw={"placeholder": "Favorite Color"})
    password_hash = PasswordField("", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')], render_kw={"placeholder": "Password"})
    password_hash2 = PasswordField("", validators=[DataRequired()], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Submit")
    # abc = StringField('abc', [InputRequired()], render_kw={"placeholder": "test"})
# -- Post Form --
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author")
    slug = StringField("Slug Field", validators=[DataRequired()])
    submit = SubmitField("Submit")
# -- Login Form --
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
# -- Search Form --
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")
