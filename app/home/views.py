import urllib, hashlib, base64
from . import home
from app import app, db, models, forms, bcrypt
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, g, session
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound

''' User Experience '''

@home.route("/signup", methods=['GET', 'POST'])
def signup():
    form = forms.SignupForm();
    if form.validate_on_submit():
        new_user = models.User(name=form.name.data, email=form.email.data, password=bcrypt.generate_password_hash(base64.urlsafe_b64encode(hashlib.sha256(form.password.data.encode("utf-8")).digest())), SSO=False)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect('/')
    return render_template('signup.html', form=form)

@home.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = db.session.query(models.User).filter(models.User.email==form.email.data).one()
        except NoResultFound:
            flash("Email is not valid. Please try again")
            return render_template('login.html', form=form)
        if not bcrypt.check_password_hash(user.password, base64.urlsafe_b64encode(hashlib.sha256(form.password.data.encode("utf-8")).digest())):
            flash("Email and password do not match. Please try again.")
            return render_template('login.html', form=form)
        if (form.remember_me.data):
            login_user(user, remember = True)
        else:
            login_user(user)
        return form.redirect('index')
    return render_template('login.html', form=form)

@home.route('/reauthenticate', methods=['GET', 'POST'])
@login_required
def reauthenticate():
    form = forms.ReauthenticateForm()
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, base64.urlsafe_b64encode(hashlib.sha256(form.password.data.encode("utf-8")).digest())):
            flash("Password is incorrect. Please try again.")
            return render_template('reauth.html', form=form)
        login_user(current_user, remember=True)
        return form.redirect(url_for('home.index'))
    return render_template('reauth.html', user=current_user, form=form)

#TODO: Logout deletes current device's cookies
@home.route('/logout')
@login_required
def logout():
    try:
        db.session.delete(session['cookie'])
        del session['cookie']
        db.session.commit()
    except KeyError:
        pass
    logout_user()
    return redirect(url_for('home.index'))

''' Index '''

@home.route('/')
@home.route("/index")
def index():
    return render_template("index.html")

@home.route("/about")
def about():
    return render_template("about.html")

@home.route("/class")
def classes():
    query = models.Search.query.filter(models.Search.role=="class").all()
    classes = []
    for x in query:
        classes.append((x.name0, x.name1))
    return render_template("classlist.html", classes=classes)

@home.route("/autocomplete", methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    dept = request.args.get('d')
    role = request.args.get('r')
    #print(search+', ' + dept + ', ' + role)
    return jsonify(matching_results=models.Search.autosearch(querystring=search, dept=dept, role=role))

@home.route("/search/<query>")
def search(query):
    result = urllib.parse.unquote(query)
    if (models.Search.query.filter(models.Search.name0==result).first() is None):
        dbquery = models.Search.query.filter(models.Search.name1==result).first()
        dbquery.hits += 1
        db.session.commit()
        if (dbquery.role == "class"):
            name = dbquery.name0.split()
            return redirect(url_for('dept.classpage', dept=name[0], classnum=name[1]))
        elif (db.role == "department"):
            name = dbquery.name0
            return redirect(url_for('dept.departmentpage', dept=name))
        else:
            query = query.replace(" ", "")
            return redirect(url_for("prof.professorpage", professor=query))
    else:
        dbquery = models.Search.query.filter(models.Search.name0==result).first()
        dbquery.hits += 1
        db.session.commit()
        if (dbquery.role == "class"):
            query = dbquery.name0.split()
            return redirect(url_for('dept.classpage', dept=name[0], classnum=name[1]))
        elif (dbquery.role == "department"):
            return redirect(url_for('dept.departmentpage', dept=query))
        else:
            query = query.replace(" ", "")
            return redirect(url_for("prof.professorpage", professor=query))
