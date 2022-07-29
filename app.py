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


def list_pictures(dir):
    pictures = os.listdir(dir)
    return pictures

def delete_everything(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


# -=-=-=-=-=- DataBase Queries Here -=-=-=-=-=-
def get_pictures(phone):
    SQLget = f" SELECT picture FROM dima.dbo.picture WHERE number = '{phone}'"
    try:
        delete_everything(dir)
        cursor.execute(SQLget)
        myresult = cursor.fetchall()
        i = 1
        for row in myresult:
            name = str(phone) + "-" + str(i)
            result = row[0]
            storedimagepath = f"static/images/img{name}.jpg"
            with open(storedimagepath, "wb") as file:
                file.write(result)
                i += 1
                file.close()
    except Exception as e:
        print(e)

def add_pictures(phone, picture):
    SQLinsert = f" INSERT INTO dima.dbo.picture (number, picture) values (?, ?)"
    try:
        cursor.execute(SQLinsert, (phone, picture))
        conn.commit()
    except Exception as e:
        print(e)
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
    directory = dir
    if form.validate_on_submit():
        # Get Data From Submitted Search
        number = form.searched.data
        # Query The DataBase
        get_pictures(phone=number)
        pictures = list_pictures(dir)
        return render_template("search.html", form=form, searched=number, pictures=pictures)
    else:
        flash("Please Write Something In The Search Bar")
        return render_template("search.html", form=form, searched=number)

