from app import db, models
import csv, glob

f = open("extract.csv", "r")
read = csv.reader(f, delimiter=",")
i = 0
for line in read:
    if i != 0:
        if len(line) is 7:
            db.session.add(models.Reviews(professorname=line[1], classname=line[2], comments=line[3], date=line[6], quality=line[4], easy=line[5]))
        else:
            db.session.add(models.Reviews(professorname=line[1], classname=line[2], comments=line[3]))
    i += 1

db.session.commit()
