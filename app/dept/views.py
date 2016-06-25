from flask import Blueprint, render_template
from app import db, models
from . import dept

@dept.route('/<dept>')
@dept.route('/<dept>/<int:page>')
def departmentlist(dept):#, page=1):
    department = dept.upper()
    classes = db.session.query(models.Search).filter(models.Search.name0.like(str(department) + " " +"%")).order_by(models.Search.name0).all()
    #classes = classes.paginate(1, 20, False).items
    professors = db.session.query(models.Search).filter(models.Search.dept==str(department)).order_by(models.Search.name0).all()
    #professors= professors.paginate(1,20, False).items
    links_classes = []
    links_professors = []
    for x in classes:
        temp = x.name0.split()
        links_classes.append((x.name0, x.name1,"/dept/"+temp[0]+"/class/"+temp[1]))
    for x in professors:
        temp = x.name0.replace(" ", "")
        links_professors.append((x.name0, "/professor/" + temp))
    return render_template("departmentlist.html", departmentname = str(department), links_classes=links_classes, links_professors=links_professors)

@dept.route('/<dept>/class/<classnum>')
def classthing(dept, classnum):
    department = dept.upper()
    reviews = db.session.query(models.Reviews).filter(models.Reviews.classname==(str(department) + " " + str(classnum)))
    stats = [db.session.query(db.func.avg(models.Reviews.easy)).filter(models.Reviews.classname==(str(department) + " " + str(classnum)))[0],
            db.session.query(db.func.avg(models.Reviews.quality)).filter(models.Reviews.classname==(str(department) + " " + str(classnum)))[0]]
    professors = []
    for x in reviews.order_by(models.Reviews.professorname).distinct(models.Reviews.professorname):
        professors.append(x.professorname)
    return render_template("class.html", classname = str(department) + " " + str(classnum), reviews=reviews.order_by(models.Reviews.date.desc()), stats=stats, professors=professors)
