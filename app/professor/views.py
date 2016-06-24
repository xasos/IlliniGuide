from flask import Blueprint, render_template
from app import db, models
from . import prof

def addspace(coursecode):
    y=0
    for x in coursecode:
        if x.isupper() and x is not coursecode[0]:
            break
        y+=1
    return coursecode[0:y] + " " + coursecode[y:]

@prof.route('/<professor>')
def stuff(professor):
    professor = addspace(professor)
    reviews = db.session.query(models.Reviews).filter(models.Reviews.professorname==(str(professor)))
    stats = [db.session.query(db.func.avg(models.Reviews.easy)).filter(models.Reviews.professorname==(str(professor)))[0],
              db.session.query(db.func.avg(models.Reviews.quality)).filter(models.Reviews.professorname==(str(professor)))[0]]
    classes = []
    for x in reviews.order_by(models.Reviews.classname).distinct(models.Reviews.classname):
        classes.append(x.classname)
    return render_template("profpage.html", professorname = str(professor), reviews=reviews.order_by(models.Reviews.date.desc()), stats=stats, classes=classes)
