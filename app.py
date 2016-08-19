
# import the Flask class from slask module
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from functools import wraps
import sqlite3
import os
from config import Config  # import the Config class from module config

#


# create the application object
app = Flask(__name__)

# app.config.from_object(os.environ['APP_SETTINGS']) # application configuration
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.database = "posts.db"
app.secret_key = "This-is-confidential"

# create and config the database object
db = SQLAlchemy(app)

from models import *


# login required decorator
def login_required(f):
    # replace user current role
    @wraps(f)
    def wrap(*args, **kwargs):

        # return the current role if the user is authenticated
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


# use  decorators to link a function to url
@app.route('/dashboard')
@login_required  # a user is required to login
def home():
    return render_template('index.html')


# home route
@app.route('/')
def welcome():
    # Read from database
    posts = PostIdea.query.all()

    # Check if logged in
    if 'logged_in' in session:
        return render_template('index.html', posts=posts)
    else:
        return render_template("homepage.html", posts=posts)  # render a template


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = []
    if request.method == 'POST':
        POST_EMAIL = str(request.form['email'])
        POST_PASSWORD = str(request.form['password'])

        # create a variable query to represent the db config
        query = User.query.filter(User.email.in_([POST_EMAIL]), User.password.in_([POST_PASSWORD]))
        result = query.first()
        if result:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error.append('wrong password!')

    return render_template('login.html', error=error)


# logout route
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)  # pops out the True value of session and deletes the key(logged_in))
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # import ipdb; ipdb.set_trace()

    # validate the user's information against the defined PostIdea schema
    form = RegistrationForm(request.form, PostIdea)
    if request.method == 'POST' and form.validate():
        user = User(name=request.form['username'], password=request.form['password'], email=request.form['email'])

        # automatically adds the user to the database(db)
        db.session.add(user)

        # save the changes to the db
        db.session.commit()
        return redirect(url_for('home'))

        # if registration is unsuccessful, render the registration form
    return render_template('register.html', form=form)


# route for changing the db after login
@app.route('/post/<id>', methods=['GET', 'POST'])
@login_required
def post(data):
    if request.method == 'GET':

        data = PostIdea.query.get(id)
        print data
        if session['logged_in'] == True:
            return render_template('post.html', data=data)


# Posting an idea
@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = RegistrationForm(request.form, PostIdea)
    if request.method == 'POST':
        post = PostIdea(title=request.form['title'], description=request.form['description'])

        db.session.add(post)

        # save the changes to the db
        db.session.commit()
    return render_template('add_post.html')


# connect to the application's db
def connect_db():
    return sqlite3.connect(app.database)


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True)