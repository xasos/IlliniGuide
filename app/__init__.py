import os

from flask import Flask, session, g, render_template
from .home import home
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.register_blueprint(home)
#db = SQLAlchemy(app)
