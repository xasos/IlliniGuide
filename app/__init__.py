import os, base64, hashlib
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.contrib.fixers import ProxyFix
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object('config')

app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

from .home import home
from .professor import prof
from .dept import dept

app.register_blueprint(home)
app.register_blueprint(prof)
app.register_blueprint(dept)

#from flask_dance.contrib.google import make_google_blueprint, google

#blueprint = make_google_blueprint(
#    client_id="my-key-here",
#    client_secret="my-secret-here",
#    scope=["profile", "email"]
#)
#
#app.register_blueprint(blueprint, url_prefix="/google")

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_serializer = URLSafeTimedSerializer(app.secret_key)
login_manager.login_view = '/login'
login_manager.refresh_view = "/reauthenticate"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.token_loader
def load_token(token):
    try:
        loaded_token = login_serializer.loads(token, max_age=604800)
    except BadSignature:
        return None
    except SignatureExpired:
        loaded_token = login_serializer.loads(token)
        cookie = db.session.query(models.Cookie).filter(models.Cookie.selector==base64.b64decode(utf.encode(loaded_token[0])))
        db.session.delete(cookie)
        db.session.commit()
    try:
        cookie = db.session.query(models.Cookie).filter(models.Cookie.selector==base64.b64decode(utf.encode(loaded_token[0]))).one()
    except NoResultsFound:
        return None
    if (hashlib.sha256(base64.b64decode(utf.encode(loaded_token[1]))).digest() != cookie.validator):
        db.session.delete(cookie)
        db.session.commit()
        return None
    return cookie.User
