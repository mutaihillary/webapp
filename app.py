
# import the Flask class from slask module
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from functools import wraps
import sqlite3
import os


# create the application object
app = Flask(__name__)

# app.config.from_object(os.environ['APP_SETTINGS']) # application configuration
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.database = "posts.db"
app.secret_key = "This-is-confidential"

db = SQLAlchemy(app)



