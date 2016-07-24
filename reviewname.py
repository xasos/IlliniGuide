from app import db, models
from fuzzywuzzy import fuzz, process
import csv

subjects = {}
bad=[]
todo = []

depts = db.session.query(models.Search).filter(models.Search.role=='department')
for x in depts.all():
    subjects[x.name1] = x.name0

f = open('data/professors3.csv', 'r', encoding='WINDOWS-1252')
read = csv.reader(f, delimiter=',')

new_lines = []
i=0
for line in read:
    if i != 0:
        department = line[1].split(',')[0]
        test = process.extractOne(department, list(subjects.keys()))
        if test[1] > 95:
            new_lines.append([line[0], subjects[test[0]], line[2], line[3], line[4], line[5], line[6], line[7], line[8]])
        else:
            new_lines.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8]])
    i+=1

f = open('data/professors4.csv', 'w')
write = csv.writer(f)

for lines in new_lines:
    write.writerow(lines)



'''for x in db.session.query(models.Reviews).all():
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
'''
