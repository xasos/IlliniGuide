from flask import Blueprint, render_template, jsonify, request, redirect
from . import home
from app import db, models
from operator import itemgetter
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
    query = db.session.query(models.Search).filter(models.Search.name0.ilike('%' + str(search) + '%')).order_by(models.Search.hits.desc())
    query2 = db.session.query(models.Search).filter(models.Search.name1.ilike('%' + str(search) + '%')).order_by(models.Search.hits.desc())
    results = []
    results2 = []
    for mv in query:
        results.append((mv.name0, mv.hits))
    for mv in query2:
        results.append((mv.name1, mv.hits))
    results = sorted(results, key=itemgetter(1), reverse=True)
    for mv in results:
        results2.append(mv[0])
    return jsonify(matching_results=results2)

@home.route("/search/<query>")
def search(query):
    result = urllib.parse.unquote(query)
    if (models.Search.query.filter_by(name0=result).first() is None):
        dbquery = models.Search.query.filter_by(name1=result).first()
        dbquery.hits += 1
        db.session.commit()
        if (dbquery.role == "class"):
            name = dbquery.name0.split()
            return redirect("/dept/"+name[0]+"/class/"+name[1])
        elif (db.role == "department"):
            name = dbquery.name0
            return redirect("/dept/"+name)
        else:
            query = query.replace(" ", "")
            return redirect("/professor/"+query)
    else:
        dbquery = models.Search.query.filter_by(name0=result).first()
        dbquery.hits += 1
        db.session.commit()
        if (dbquery.role == "class"):
            query = dbquery.name0.split()
            return redirect("/dept/"+query[0]+"/class/"+query[1])
        elif (dbquery.role == "department"):
            return redirect("/dept/"+query)
        else:
            query = query.replace(" ", "")
            return redirect("/professor/"+query)
