from flask import Blueprint, render_template, jsonify, request, redirect
from . import home
from app import db, models
import urllib

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

@home.route("/search/<query>")
def search(query):
    result = urllib.parse.unquote(query)

    if (models.searchtest.query.filter_by(name=result).first().role == "class"):
        query = query.split()
        return redirect("/dept/"+query[0]+"/class/"+query[1])
    elif (models.searchtest.query.filter_by(name=result).first().role == "dept"):
        return redirect("/dept/"+query)
    else:
        query = query.replace(" ", "")
        return redirect("/professor/"+query)
