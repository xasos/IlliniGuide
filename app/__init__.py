import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from .home import home
from .professor import prof

app.register_blueprint(home)
app.register_blueprint(prof)
