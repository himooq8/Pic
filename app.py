import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for
import pyodbc as dbb
import sys
from webforms import *
import os

# -=-=-=-=-=- DataBase Connection Starts Here -=-=-=-=-=-
DRIVER = 'SQL Server'
SERVER_NAME = 'HiMoO'
DATABASE_NAME = 'dima'
Uid = 'python'
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


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-  Static Imagee File Directory -=-=-=-=-=-=-=-=-=-
dir = "C:/Users/S/Desktop/Projects/Pic/static/images"
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-



# -=-=-=-=-=- DataBase Queries Here -=-=-=-=-=-
def get_pictures(phone):
    SQLget = f" SELECT id, picture FROM dima.dbo.picture WHERE number = '{phone}'"
    result = []
    try:
        cursor.execute(SQLget)
        result = [{'id': row[0], 'path': row[1]} for row in cursor.fetchall()]
    except Exception as e:
        print(e)
    return result


def get_last(phone):
    SQLget = f"SELECT pic_num FROM dima.dbo.picture WHERE number = '{phone}' ORDER BY id DESC"
    try:
        cursor.execute(SQLget)
        result = cursor.fetchone()
        return result[0] if result is not None else 0
    except Exception as e:
        print(str(e))


def add_pictures(phone, picture, pic_num):
    SQLinsert = f" INSERT INTO dima.dbo.picture (number, picture, pic_num) values (?, ?, ?)"
    try:
        ext = picture.filename.split('.')[-1]
        if ext not in ('jpg', 'jpeg', 'png'):
            ext = 'jpg'
        path = f'static/images/img{phone}-{pic_num}.{ext}'
        with open(f'{path}', 'wb') as f:
            f.write(picture.read())
        cursor.execute(SQLinsert, (phone, path, pic_num))
        conn.commit()
    except Exception as e:
        print(e)
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
                last_id = get_last(number)
                add_pictures(phone=number, picture=picture, pic_num=last_id+1)
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
    directory = dir
    if form.validate_on_submit():
        # Get Data From Submitted Search
        number = form.searched.data
        # Query The DataBase
        pictures = get_pictures(phone=number)
        return render_template("search.html", form=form, searched=number, pictures=pictures)
    else:
        flash("Please Write Something In The Search Bar")
        return render_template("search.html", form=form, searched=number)

