from flask import Blueprint, render_template
from app import db, models
from . import user
from flask_login import current_user, login_required, fresh_login_required

@user.route('/<user>')
@login_required
def userpage(user):
    return user
