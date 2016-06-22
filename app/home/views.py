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
    return render_template("about.html")

@home.route("/autocomplete", methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = db.session.query(models.Search.name0).filter(models.Search.name0.ilike('%' + str(search) + '%'))
    query2 = db.session.query(models.Search.name1).filter(models.Search.name1.ilike('%' + str(search) + '%'))
    results = [mv[0] for mv in query.all()]
    for mv in query2.all():
        results.append(mv[0])
    return jsonify(matching_results=results)

@home.route("/search/<query>")
def search(query):
    result = urllib.parse.unquote(query)

    if (models.Search.query.filter_by(name0=result).first() is None):
        if (models.Search.query.filter_by(name1=result).first().role == "class"):
            query = models.Search.query.filter_by(name1=result).first().name0
            query = query.split()
            return redirect("/dept/"+query[0]+"/class/"+query[1])
        elif (models.Search.query.filter_by(name1=result).first().role == "department"):
            query = models.Search.query.filter_by(name1=result).first().name0
            return redirect("/dept/"+query)
        else:
            query = query.replace(" ", "")
            return redirect("/professor/"+query)
    else:
        if (models.Search.query.filter_by(name0=result).first().role == "class"):
            query = query.split()
            return redirect("/dept/"+query[0]+"/class/"+query[1])
        elif (models.Search.query.filter_by(name0=result).first().role == "department"):
            return redirect("/dept/"+query)
        else:
            query = query.replace(" ", "")
            return redirect("/professor/"+query)
