import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for
import pyodbc as dbb
import sys
from sqlalchemy.engine import URL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from datetime import datetime
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import *

# -=-=-=-=-=- DataBase Connection Starts Here -=-=-=-=-=-
DRIVER = 'SQL Server'
SERVER_NAME = 'GCC-KW-IT-03'
DATABASE_NAME = 'PythonTesting'
Uid = 'sa'
Pwd = 'Sharhan@12'

connection = f"DRIVER={DRIVER};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={Uid};PWD={Pwd}"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection})

engine = create_engine(connection_url)
# -=-=-=-=-=- DataBase Connection Ends Here -=-=-=-=-=-
# -=-=-=-=-=- DataBase Queries Here -=-=-=-=-=-
def show_tables():
    records = pd.read_sql_query("""
        SELECT *
        FROM PythonTesting.dbo.OurList
        """, engine)
    return records

def show_content(department, table_name):
    records = pd.read_sql_query(f" SELECT * FROM AdventureWorks2019.{department[0]}.{table_name[0]}", engine)
    return records
# -=-=-=-=-=- DataBase Queries Ends Here -=-=-=-=-=-
# data = show_content(department, table_name)
# tables = pd.read_sql_table('OurList', engine)
tables = show_tables()
testt = pd.DataFrame(tables)
movie_list = testt.iloc[0]
type_list = testt.iloc[1]
year_list = testt.iloc[2]
release_list = testt.iloc[3]
# [x[1] for x in L]
# department = [x[0] for x in tables]
# table_name = [x[1] for x in tables]

# testt.iloc[0]
# movie_list = [x[0] for x in testt]
# type_list = [x[1] for x in testt]
# year_list = [x[2] for x in testt]
# release_list = [x[3] for x in testt]

# -=-=-=-=-=- FLASK App Routes Here -=-=-=-=-=-
app = Flask(__name__)
# -- Add DataBase --
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# -- Create Model (Table) --
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    data_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # -- Foreign Key To Link Users To Posts (Refer to Primary Key) --
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(50))
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    # -- Create Password Hash --
    password_hash = db.Column(db.String(128))
    # -- User Can Have Many Posts --
    posts = db.relationship('Posts', backref='poster')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    # -- Create A String --
    def __repr__(self):
        return '<Name %r>' % self.name
# -- Create Secret Key --
app.config['SECRET_KEY'] = "Your Super Password Here"
subscribers = []

# -- FLASK Login Stuff Here --
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# -- FLASK App Routes Start Here --
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

@app.route('/')
def home():
    return render_template("home.html", tables=tables,
                                        testt=testt,
                                        movie_list=movie_list,
                                        type_list=type_list,
                                        year_list=year_list,
                                        release_list=release_list)

@app.route('/about')
def about():
    names = ["1st", "2nd", "3rd", "4th", "5th"]
    return render_template("about.html", names=names)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/signup', methods=["POST"])
def signup():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

# -=-=-=-=-=- How to Send an EMAIL here -=-=-=-=-=-
#    import smtplib
#    message = "You have Signed Up for Us"
#    server = smtplib.SMTP("smtp.gmail.com", 587)
#    server.starttls()
#    server.login("m.r.alsharhan@gmail.com", "password")
#    server.sendmail("m.r.alsharhan@gmail.com", email, message)

    if not first_name or not last_name or not email or not password:
        error_statement = "All Fields Required ..."
        return render_template("fail.html",
                               error_statement=error_statement,
                               first_name=first_name,
                               last_name=last_name,
                               email=email,
                               password=password)
    subscribers.append(f"{first_name} {last_name} || {email}")
    return render_template("signup.html", subscribers=subscribers)

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Welcome To Our Form")
    return render_template("name.html", name=name, form=form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hashing the Password First
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, username=form.username.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        # form.password_hash2.data = ''
        flash("You Registered Successfully!")
    our_users = Users.query.order_by(Users.data_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("There Was An Error")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    name = None
    form = UserForm()
    name_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("User Deleted")
        our_users = Users.query.order_by(Users.data_added)
        return render_template("add_user.html", name=name, form=form, our_users=our_users)
    except:
        flash("There Was An Error")
        return render_template("add_user.html", name=name, form=form, our_users=our_users)

@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clearing Form Fields
        form.email.data = ''
        form.password_hash.data = ''
        # Look-Up Users by Email in DB
        pw_to_check = Users.query.filter_by(email=email).first()
        # Check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash, password)
    return render_template("test_pw.html", email=email, form=form, password=password, pw_to_check=pw_to_check, passed=passed)

@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data,
                     content=form.content.data,
                     poster_id=poster,
                     slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit()
        flash("Post Submitted")
    return render_template("add_post.html", form=form)

@app.route('/posts')
def posts():
    # Grab all posts from DB
    posts = Posts.query.order_by(Posts.data_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    # Grab all posts from DB
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    # Grab all posts from DB
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update the DataBase
        db.session.add(post)
        db.session.commit()
        flash("Post Updated!")
        return redirect(url_for('post', id=post.id))
    if current_user.id == post.poster_id:
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template("edit_post.html", form=form)
    else:
        flash("Access Denied!")
        posts = Posts.query.order_by(Posts.data_posted)
        return render_template("posts.html", posts=posts)

@app.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    # Grab all posts from DB
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post Deleted!")
            posts = Posts.query.order_by(Posts.data_posted)
            return render_template("posts.html", posts=posts)
        except:
            flash("Something Went Wrong")
            posts = Posts.query.order_by(Posts.data_posted)
            return render_template("posts.html", posts=posts)
    else:
        flash("Access Denied!")
        posts = Posts.query.order_by(Posts.data_posted)
        return render_template("posts.html", posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check User Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Email or Password")
        else:
            flash("User Doesnt Exist")
    return render_template("login.html", form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
        except:
            flash("There Was An Error")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out")
    return redirect(url_for('login'))

# -=-=-=-=-=- Search Function Here -=-=-=-=-=-
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get Data From Submitted Search
        post.searched = form.searched.data
        # Query The DataBase
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template("search.html", form=form, posts=posts, searched=post.searched)
    else:
        flash("Please Write Something In The Search Bar")
        return render_template("search.html", form=form, posts=posts, searched=post.searched)

# -=-=-=-=-=- Pass stuff To NavBar (Header.html) -=-=-=-=-=-
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

