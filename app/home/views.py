from flask import Blueprint, render_template, jsonify, request
from . import home
from app import db, models

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

@home.route("/autocomplete", methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = db.session.query(models.searchtest.name).filter(models.searchtest.name.like('%' + str(search) + '%'))
    results = [mv[0] for mv in query.all()]
    return jsonify(matching_results=results)
