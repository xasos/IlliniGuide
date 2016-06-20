from flask import Blueprint, render_template, jsonify
from . import home

@home.route('/')
@home.route("/index")
def index():
    return render_template("index.html")

#@home.route('/login')
#def login():
#    pass
#
#@home.route("/logout")
#def logout():
#    pass
#
#@home.route("/signup")
#def signup():
#    pass

@home.route("/about")
def about():
    pass

@home.route("/autocomplete")
def autocomplete():
    pass
