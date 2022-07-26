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
SERVER_NAME = 'LAPTOP-CMISMCVF'
DATABASE_NAME = 'dima'
Uid = 'alsharhan'
Pwd = 'Himoo@123'

Connection = f"""
    Driver={DRIVER};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
    Uid={Uid};
    Pwd={Pwd};
"""
try:
    conn = dbb.connect(Connection)
except Exception as e:
    print(e)
    print('Test Failed')
    sys.exit()
else:
    cursor = conn.cursor()
# -=-=-=-=-=- DataBase Connection Ends Here -=-=-=-=-=-
# -=-=-=-=-=- DataBase Queries Here -=-=-=-=-=-

def get_pictures(phone):
    print('Show Content')
    # cursor = conn.cursor()
    cursor.execute(f" SELECT picture FROM dima.dbo.picture WHERE number='{phone}'")
    records = ''
    records = cursor.fetchall()
    return records

def add_pictures(phone, picture):
    print('Show Content')
    # cursor = conn.cursor()
    cursor.execute(f" INSERT INTO picture (number, picture) values (?, ?)", (phone, picture))
    conn.commit()
    return

# -=-=-=-=-=- DataBase Queries Ends Here -=-=-=-=-=-


# -=-=-=-=-=- FLASK App Routes Here -=-=-=-=-=-
app = Flask(__name__)
app.config["SECRET_KEY"] = "Secret"

# -- FLASK App Routes Start Here --
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

# @app.route('/')
# def home():
#    return render_template("home.html")


# @app.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
# def delete_post(id):
#    # Grab all posts from DB
#    post_to_delete = Posts.query.get_or_404(id)
#    try:
#        db.session.delete(post_to_delete)
#        db.session.commit()
#        flash("Post Deleted!")
#        posts = Posts.query.order_by(Posts.data_posted)
#        return render_template("posts.html", posts=posts)
#    except:
#        flash("Something Went Wrong")
#        posts = Posts.query.order_by(Posts.data_posted)
#        return render_template("posts.html", posts=posts)

# def show_tables():
#    records = pd.read_sql_query("""
#        SELECT *
#        FROM dima.dbo.pictures
#        """, engine)
#    return records

# -=-=-=-=-=- Search Function Here -=-=-=-=-=-
@app.route('/', methods=['GET', 'POST'])
def add():
    picture_form = PhotoForm()
    search_form = SearchForm()
    if request.method == 'POST':
        if picture_form.validate_on_submit():
            # Query The DataBase
            number = picture_form.number.data
            picture = picture_form.picture.data
            try:
                add_pictures(phone=number, picture=picture.read())
                flash("Picture Added Successfully")
                return render_template("home.html", picture_form=picture_form, search_form=search_form)
            except:
                flash("There Was An Error")
                return render_template("home.html", picture_form=picture_form, search_form=search_form)
        else:
            flash("Please Write Something In The Search Bar")
            return render_template("home.html", picture_form=picture_form, search_form=search_form)
    else:
        return render_template("home.html", picture_form=picture_form, search_form=search_form)

# -=-=-=-=-=- Pass stuff To NavBar (Header.html) -=-=-=-=-=-
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    number = ''
    if form.validate_on_submit():
        # Get Data From Submitted Search
        number = form.searched.data
        # Query The DataBase
        pictures = get_pictures(phone=number)
        return render_template("search.html", form=form, pictures=pictures, searched=number)
    else:
        flash("Please Write Something In The Search Bar")
        return render_template("search.html", form=form, searched=number)

# @app.route('/search', methods=['GET', 'POST'])
# def searching():
#    search_form = SearchForm()
#    photo_form = PhotoForm()
#    if request.method == 'POST':
#        n = search_form.searched.data
#        form = photo_form.data
#        if form.is_valid():
#            photo = form.save(commit=False)
#            photo.save()
#            return render_template("search.html", search_form=search_form, photo_form=photo_form, n=n, form=form)
#        return render_template("search.html", search_form=search_form, photo_form=photo_form, n=n, form=form)
#    n = search_form.searched.data
#    filtered = n.objects.filter(number=n) if n else None
#    return render_template("search.html", search_form=search_form, photo_form=photo_form, n=n, filtered=filtered)
