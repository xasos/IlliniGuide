from flask import Blueprint, render_template
from app import db, models
from . import prof

def findname(name):
    query = db.session.query(models.Search).filter(models.Search.role=="professor")
    for x in query:
        if name.lower() == x.name0.replace(" ", "").lower():
            return x.name0
    return ""

@prof.route('/<professor>')
def stuff(professor):
    professor = findname(professor)
    if professor == "":
        abort(404)
    reviews = db.session.query(models.Reviews).filter(models.Reviews.professorname==(str(professor)))
    stats = [db.session.query(db.func.avg(models.Reviews.easy)).filter(models.Reviews.professorname==(str(professor)))[0],
              db.session.query(db.func.avg(models.Reviews.quality)).filter(models.Reviews.professorname==(str(professor)))[0]]
    classes = []
    for x in reviews.order_by(models.Reviews.classname).distinct(models.Reviews.classname):
        classes.append(x.classname)
    return render_template("profpage.html", professorname = str(professor), reviews=reviews.order_by(models.Reviews.date.desc()), stats=stats, classes=classes)
