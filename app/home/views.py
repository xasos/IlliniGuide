import urllib, hashlib, base64
from . import home
from app import db, models
from flask import Blueprint, render_template, jsonify, request, redirect
from flask_login import current_user, login_required, login_user, logout_user

''' User Experience '''

@home.route("/signup")
def signup():
    form = SignupForm();
    if form.validate_on_submit():
        new_user = User(name=form.name, email=form.email,\
                    password=bcrypt.generate_password_hash(base64.urlsafe_b64encode(hashlib.sha256(b'form.password').digest())))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect('/')
    return render_template('signup.html', form=form)

@home.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = db.session.query(models.User).filter(models.User.email==form.email).one()
        except NoResultsFound:
            flash("Email is not valid. Please try again")
            return render_template('login.html', form=form)
        if not bcrypt.check_password_hash(user.password, base64.urlsafe_b64encode(hashlib.sha256(b'form.password').digest())):
            flash("Email and password do not match. Please try again.")
            return render_template('login.html', form=form)
        if (form.remember_me):
            login_user(user, remember = True)
        else:
            login_user(user)
        return form.redirect('index')
    return render_template('login.html', form=form)

@home.route('/reauthenticate')
@login_required
def reauthenticate():
    form = ReauthenticateForm()
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, form.password):
            flash("Password is incorrect. Please try again.")
            return render_template('reauth.html', form=form)
        login_user(current_user, remember=True)
        return form.redirect('index')
    return render_template('reauth.html', user=current_user, form=form)

#TODO: Logout deletes current device's cookies
@home.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

''' Index '''

@home.route('/')
@home.route("/index")
def index():
    return render_template("index.html")

@home.route("/about")
def about():
    return render_template("about.html")

@home.route("/autocomplete", methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    return jsonify(matching_results=models.Search.autosearch(search))

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
