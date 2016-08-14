from flask import Blueprint

prof = Blueprint('prof', __name__, url_prefix="/professor", template_folder="templates", static_folder = "static", static_url_path='/static/professor')

from . import views
