from distutils.log import debug
from enum import unique
from re import template
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']='b5582691d7539acfc9d4771d'
##app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///son.db '
db= SQLAlchemy(app)

from market import routes
