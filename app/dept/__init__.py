from flask import Blueprint

dept = Blueprint('dept', __name__, url_prefix="/dept", template_folder="templates", static_folder = "static")

from . import views
