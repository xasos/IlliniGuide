''' App Initialization '''

from flask import Flask, flash, g, session
from werkzeug.contrib.fixers import ProxyFix
import os

app = Flask(__name__)
app.config.from_object('config')
if (os.path.isfile(os.path.join(os.path.dirname(__file__), '../config.py'))):
    app.config.from_object('config2')

app.wsgi_app = ProxyFix(app.wsgi_app)

''' Extension Init '''

from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer

bcrypt = Bcrypt(app)
login_serializer = URLSafeTimedSerializer(app.secret_key)

''' Database and Migrations '''

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#TODO: App Factory?
db = SQLAlchemy(app)
#db.Model.metadata.reflect(db.engine)
meta = db.Model.metadata
engine = db.engine

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

''' Blueprints '''

from .home import home
from .professor import prof
from .dept import dept
from .user import user

app.register_blueprint(home)
app.register_blueprint(prof)
app.register_blueprint(dept)
app.register_blueprint(user)

''' Local Users, Login, and Cookie Handling '''

import base64, hashlib
from flask_login import LoginManager, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound

#from flask_bcrypt import Bcrypt

login_manager = LoginManager(app)

login_manager.login_view = '/login'
login_manager.refresh_view = '/reauthenticate'
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@login_manager.token_loader
def load_token(token):
    print("Loading Token")
    try:
        loaded_token = login_serializer.loads(token, max_age=1)
    except BadSignature:
        return None
    except SignatureExpired:
        loaded_token = login_serializer.loads(token)
        cookie = db.session.query(models.Cookie).filter(models.Cookie.selector==base64.b64decode(utf.encode(loaded_token[0])))
        db.session.delete(cookie)
        db.session.commit()
        return None
    try:
        cookie = db.session.query(models.Cookie).filter(models.Cookie.selector==base64.b64decode(utf.encode(loaded_token[0]))).one()
    except NoResultFound:
        return None
    if (hashlib.sha256(base64.b64decode(utf.encode(loaded_token[1]))).digest() != cookie.validator):
        db.session.delete(cookie)
        db.session.commit()
        return None
    return cookie.User

''' OAuth '''

import blinker
from app import models
from flask_login import current_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error

google_blueprint = make_google_blueprint(
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    scope=["profile", "email"],
    redirect_url='/'
)
app.register_blueprint(google_blueprint, url_prefix="/login")
google_blueprint.backend = SQLAlchemyBackend(models.GoogleOAuth, db.session, user=current_user)

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(google_blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=google_blueprint.name))
        return
    resp = google_blueprint.session.get("/plus/v1/people/me")
    if resp.ok:
        email = resp.json()["emails"][0]["value"]
        query = models.User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = models.User(name=resp.json()["displayName"], email=resp.json()["emails"][0]["value"], SSO=True, SSOProvider="Google")
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash("Successfully signed in with Google")
    else:
        msg = "Failed to fetch user info from {name}".format(name=google_blueprint.name)
        flash(msg, category="error")

@oauth_error.connect_via(google_blueprint)
def google_error(google_blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=google_blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")

fb_blueprint = make_facebook_blueprint(
    client_id=app.config['FACEBOOK_CLIENT_ID'],
    client_secret=app.config['FACEBOOK_CLIENT_SECRET'],
    scope=["public_profile", "email"]
)
app.register_blueprint(fb_blueprint, url_prefix="/login")
fb_blueprint.backend = SQLAlchemyBackend(models.FacebookOAuth, db.session, user=current_user)

@oauth_authorized.connect_via(fb_blueprint)
def fb_logged_in(fb_blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=fb_blueprint.name))
        return
    resp = fb_blueprint.session.get("/2.6/me?fields=name,email")
    if resp.ok:
        email = resp.json()["email"]
        query = models.User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = modelsUser(name=resp.json()["name"], email=resp.json()["emails"], SSO=True, SSOProvider="Facebook")
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash("Successfully signed in with Facebook")
    else:
        msg = "Failed to fetch user info from {name}".format(name=fb_blueprint.name)
        flash(msg, category="error")

@oauth_error.connect_via(fb_blueprint)
def fb_error(fb_blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=fb_blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")
