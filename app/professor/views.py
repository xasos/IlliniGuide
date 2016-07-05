from flask import Blueprint, render_template
from app import db, models, forms
from . import prof

def findname(name):
    query = db.session.query(models.Search).filter(models.Search.role=="professor")
    for x in query:
        if name.lower() == x.name0.replace(" ", "").lower():
            return x.name0
    return ""

@prof.route('')
@prof.route('/')
def professorlist():
    query = models.Search.query.filter(models.Search.role=="professor").all()
    profs = []
    for x in query:
        profs.append(x.name0)
    return render_template("allprof.html", professors=sorted(profs))

@prof.route('/<professor>')
def professorpage(professor):
    professor = findname(professor)
    if professor == "":
        abort(404)
    reviews = db.session.query(models.Reviews).filter(models.Reviews.professorname==(str(professor)))
    stats = [("Easiness", db.session.query(db.func.avg(models.Reviews.easy)).filter(models.Reviews.professorname==(str(professor)))[0]),
              ("Overall Quality", db.session.query(db.func.avg(models.Reviews.quality)).filter(models.Reviews.professorname==(str(professor)))[0])]
    classes = []
    for x in reviews.order_by(models.Reviews.classname).distinct(models.Reviews.classname):
        classes.append(x.classname)
    return render_template("profpage.html", form=forms.ReviewForm(), professorname = str(professor), reviews=reviews.order_by(models.Reviews.date.desc()), stats=stats, classes=classes)
