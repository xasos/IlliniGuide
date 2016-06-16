import os

from flask import Flask
from .home import site
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.register_blueprint(api, subdomain='home')
#db = SQLAlchemy(app)
