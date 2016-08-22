from app import app
from flask import render_template, request
from models import Category, Todo, Priority, db


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/')
def list_all():
    return render_template(
        'list.html',
        categories=Category.query.all(),
        todos=Todo.query.join(Priority).order_by(Priority.value.desc())
