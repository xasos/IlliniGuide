import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://'+os.environ['USER']+':@localhost/illiniguide')
SQLALCHEMY_TRACK_MODIFICATIONS=False
WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED', True)
SECRET_KEY = os.environ.get('SECRET_KEY')
GOOGLE_CLIENT_ID=os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET=os.environ.get('GOOGLE_CLIENT_SECRET')
FACEBOOK_CLIENT_ID=os.environ.get('FACEBOOK_CLIENT_ID')
FACEBOOK_CLIENT_SECRET=os.environ.get('FACEBOOK_CLIENT_SECRET')

REMEMBER_COOKIE_NAME="IlliniGuide-Cookie"
REMEMBER_COOKIE_DURATION=timedelta(weeks=1)
REMEMBER_COOKIE_HTTPONLY=True
REMEMBER_COOKIE_SECURE=True

'''local testing only '''

OAUTHLIB_RELAX_TOKEN_SCOPE=os.environ.get('OAUTHLIB_RELAX_TOKEN_SCOPE', 1)
OAUTHLIB_INSECURE_TRANSPORT=os.environ.get('OAUTHLIB_INSECURE_TRANSPORT', 1)
