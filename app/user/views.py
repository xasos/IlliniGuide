from flask import Blueprint, render_template
from app import db, models
from . import user
from flask_login import current_user, login_required, fresh_login_required

@user.route('/<user>')
@login_required
def userpage(user):
    return user

@user.route('/<user>/scheduler')
@login_required
def scheduler(user):
    pass

@user.route('/<user>/scheduler/auto')
@login_required
def autoschedule(user):
    pass

@user.route('/<user>/settings')
@fresh_login_required
def settings(user):
    pass

@user.route('/<user>/progress')
@login_required
def progress(user):
    pass
