from flask import Blueprint, render_template, abort
from app import db, models, forms
from . import dept
import time

@dept.route('')
@dept.route('/')
def departmentlist():
    query = models.Search.query.filter(models.Search.role=="department").all()
    departments = []
    for x in query:
        departments.append((x.name0, x.name1))
    return render_template("dept/alldept.html", departments=departments)

@dept.route('/<dept>')
@dept.route('/<dept>/<int:page>')
def departmentpage(dept):#, page=1):
    department = dept.upper()
    if (models.Search.query.filter(models.Search.role=="department").filter(models.Search.name0==department).first() is None):
        abort(404)
    classesquery = db.session.query(models.Search).filter(models.Search.name0.like(str(department) + " " +"%")).order_by(models.Search.name0).all()
    #classes = classes.paginate(1, 20, False).items
    professorsquery = db.session.query(models.Search).filter(models.Search.dept==str(department)).filter(models.Search.role=="professor").order_by(models.Search.name0).all()
    #professors= professors.paginate(1,20, False).items
    classes = []
    professors = []
    for x in classesquery:
        classes.append((x.name0, x.name1))
    for x in professorsquery:
        professors.append(x.name0)
    return render_template("dept/departmentlist.html", departmentname = str(department), classes=classes, professors=professors)

@dept.route('/<dept>/class/<classnum>', methods=['GET', 'POST'])
def classpage(dept, classnum):
    form = forms.ReviewForm()
    if form.validate_on_submit():
        db.session.add(models.UserReviews(user_id = current_user.id, professor=form.professorname.data, classname=dept+' '+classnum, profdifficulty=form.profdifficulty.data, classdifficulty=form.classdifficulty.data, groupwork=form.groupwork.data, hoursperweek=form.hoursperweek.data, grade=form.grade.data+form.plusminus.data, date=time.strftime('%d/%m/%Y')))
        db.session.commit()
    department = dept.upper()
    if (models.Search.query.filter(models.Search.role=="class").filter(models.Search.name0==department+" "+classnum).first() is None):
        abort(404)
    reviews = db.session.query(models.Reviews).filter(models.Reviews.classname==(str(department) + " " + str(classnum)))
    stats = [db.session.query(db.func.avg(models.Reviews.easy)).filter(models.Reviews.classname==(str(department) + " " + str(classnum)))[0],
            db.session.query(db.func.avg(models.Reviews.quality)).filter(models.Reviews.classname==(str(department) + " " + str(classnum)))[0]]
    professors = []
    for x in reviews.order_by(models.Reviews.professorname).distinct(models.Reviews.professorname):
        professors.append(x.professorname)
    return render_template("dept/class.html", form=form, classname = str(department) + " " + str(classnum), reviews=reviews.order_by(models.Reviews.date.desc()), stats=stats, professors=professors)
