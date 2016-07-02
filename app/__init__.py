''' App and DB Initialization '''

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_object('config')

app.wsgi_app = ProxyFix(app.wsgi_app)

#TODO: App Factory?
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

''' Blueprints '''

from .home import home
from .professor import prof
from .dept import dept

app.register_blueprint(home)
app.register_blueprint(prof)
app.register_blueprint(dept)

''' Local Users, Login, and Cookie Handling '''

import base64, hashlib
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_serializer = URLSafeTimedSerializer(app.secret_key)
login_manager.login_view = '/login'
login_manager.refresh_view = '/reauthenticate'

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

''' OAuth '''

from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import blinker

google_blueprint = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID
    client_secret=GOOGLE_CLIENT_SECRET,
    scope=["profile", "email"],
    redirect_url='/'
)
app.register_blueprint(google_blueprint, url_prefix="/login")
google_blueprint.backend = SQLAlchemyBackend(GoogleOAuth, db.session, user=current_user)

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(google_blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=google_blueprint.name))
        return
    resp = google_blueprint.session.get("/plus/v1/people/me")
    if resp.ok:
        email = resp.json()["emails"][0]["value"]
        query = User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = User(name=resp.json()["displayName"], email=resp.json()["emails"][0]["value"])
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
    client_id=FACEBOOK_CLIENT_ID
    client_secret=FACEBOOK_CLIENT_SECRET,
    scope=[public_profile, email]
)
app.register_blueprint(facebook_blueprint, url_prefix="/login")
fb_blueprint.backend = SQLAlchemyBackend(FacebookOAuth, db.session, user=current_user)

@oauth_authorized.connect_via(fb_blueprint)
def fb_logged_in(fb_blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=fb_blueprint.name))
        return
    resp = fb_blueprint.session.get("/2.6/me?fields=name,email")
    if resp.ok:
        email = resp.json()["email"]
        query = User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = User(name=resp.json()["name"], email=resp.json()["emails"])
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
