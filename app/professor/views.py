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
    return render_template("professor/allprof.html", professors=sorted(profs))

@prof.route('/<professor>', methods=['GET', 'POST'])
def professorpage(professor):
    form = forms.ReviewForm()
    professor = findname(professor)
    if form.validate_on_submit():
        db.session.add(models.UserReviews(user_id = current_user.id, professor=professor, classname=form.classname.data, profdifficulty=form.profdifficulty.data, classdifficulty=form.classdifficulty.data, groupwork=form.groupwork.data, hoursperweek=form.hoursperweek.data, grade=form.grade.data+form.plusminus.data, date=time.strftime('%d/%m/%Y')))
        db.session.commit()
    if professor == "":
        abort(404)
    reviews = db.session.query(models.Reviews).filter(models.Reviews.professorname==(str(professor)))
    stats = [("Easiness", db.session.query(db.func.avg(models.Reviews.easy)).filter(models.Reviews.professorname==(str(professor)))[0]),
              ("Overall Quality", db.session.query(db.func.avg(models.Reviews.quality)).filter(models.Reviews.professorname==(str(professor)))[0])]
    classes = []
    for x in reviews.order_by(models.Reviews.classname).distinct(models.Reviews.classname):
        classes.append(x.classname)
    return render_template("professor/profpage.html", form=form, professorname = str(professor), reviews=reviews.order_by(models.Reviews.date.desc()), stats=stats, classes=classes)
