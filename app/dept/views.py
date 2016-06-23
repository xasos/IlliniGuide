from flask import Blueprint, render_template
from app import db, models
from . import dept

@dept.route('/<dept>')
@dept.route('/<dept>/<int:page>')
def departmentlist(dept):#, page=1):
    classes = db.session.query(models.Search).filter(models.Search.name0.like(str(dept) + " " +"%")).order_by(models.Search.name0).all()
    #classes = classes.paginate(1, 20, False).items
    links_classes = []
    for x in classes:
        temp = x.name0.split()
        links_classes.append((x.name0, x.name1,"/dept/"+temp[0]+"/class/"+temp[1]))
    return render_template("departmentlist.html", links_classes = links_classes)

@dept.route('/<dept>/class/<classnum>')
def classthing(dept, classnum):
    return dept + classnum
