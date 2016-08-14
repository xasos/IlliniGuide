from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField, HiddenField, RadioField, DecimalField
from flask_wtf.html5 import DecimalRangeField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from urllib.parse import urlparse, urljoin
from flask import request, url_for, redirect

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))

class LoginForm(RedirectForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)

class SignupForm(RedirectForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

class LoginForm(RedirectForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)

class ReauthenticateForm(RedirectForm):
    password = PasswordField('Password', validators=[DataRequired()])

class ReviewForm(Form):
    professorname = StringField('Professor Name', validators=[DataRequired()])
    classname = StringField('Class Name', validators=[DataRequired()])
    comments = StringField('Comments', validators=[DataRequired()])
    profdifficulty = DecimalField('Professor Difficulty', validators=[DataRequired(), NumberRange(min=0.0, max=5.0, message='Value must be between 0.0 and 5.0')])
    classdifficulty = DecimalField('Class Difficulty', validators=[DataRequired(), NumberRange(min=0.0, max=5.0, message='Value must be between 0.0 and 5.0')])
    groupwork = DecimalField('Amount (%) of Groupwork', validators=[DataRequired(), NumberRange(min=0.0, max=100.0, message='Value must be between 0.0 and 100.0')])
    hoursperweek = DecimalField('Hours Needed per Week', validators=[DataRequired(), NumberRange(min=0.0, max=168.0, message='You can\'t spend more than a week or less than nothing in a week, pls')])
    quality = DecimalField('Overall Quality', validators=[DataRequired(), NumberRange(min=0.0, max=5.0, message='Value must be between 0.0 and 5.0')])
    grade = RadioField('Grade Received (will not be public)', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')])
    plusminus = RadioField('Plus/Minus', choices=[('Plus', '+'), ('None', ' '), ('Minus', '-')])
