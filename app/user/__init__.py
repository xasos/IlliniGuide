from flask import Blueprint

user = Blueprint('user', __name__, url_prefix="/user", template_folder="templates", static_folder = "static", static_url_path='/static/user')

from . import views
