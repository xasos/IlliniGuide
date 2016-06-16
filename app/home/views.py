from flask import Blueprint, render_template, jsonify

mod = Blueprint('home', __name__)

@mod.route('/')
@mod.route("/index")
def index():
    return render_template("index.html")

#@mod.route('/login')
#def login():
#    pass
#
#@mod.route("/logout")
#def logout():
#    pass
#
#@mod.route("/signup")
#def signup():
#    pass

@mod.route("/about")
def about():
    pass

@mod.route("/autocomplete")
def autocomplete():
    search = request.args.get('q')
    query = db_session.query(Movie.title).filter(Movie.title.like('%' + str(search) + '%'))
    results = [mv[0] for mv in query.all()]
    return jsonify(matching_results=results)
