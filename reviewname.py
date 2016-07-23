from app import db, models
from fuzzywuzzy import fuzz, process

subjects = []
bad=[]
todo = []

depts = db.session.query(models.Search).filter(models.Search.role=='department')
for x in depts.all():
    subjects.append(x.name0)

for x in db.session.query(models.Reviews).all():
    try:
        thing = x.classname.split()[0]
    except IndexError:
        bad.append(x)
        continue
    if (thing not in subjects or len(x.classname.split()) == 1):
        bad.append(x)
    if (len(x.classname.split()) > 1 and len(x.classname.split()[1]) > 3):
        bad.append(x)

print(len(bad))

for x in bad:
    print (x.professorname + ' ' + x.classname)
    if (len(x.classname.split()) > 1):
        name = x.classname.split()
        option = process.extractOne(name[0], subjects)
        if option[1] > 50:
            print(option[0])
            var = input('approve?')
            if (var == 'Y'):
                x.classname = option[0] + ' ' +name[1]
                print(x.classname)
                #db.session.commit()
                continue
            elif (var == 'S'):
                todo.append(x)
                continue
            else:
                x.classname=var
                db.session.commit()

for x in todo:
    print(x)
    var = input('done')
