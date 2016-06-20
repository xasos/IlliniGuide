from flask import Blueprint

prof = Blueprint('prof', __name__, url_prefix="/professor", template_folder="templates", static_folder = "static")

from . import views
