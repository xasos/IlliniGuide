from app import db, models
import csv

to_read = ["10-S-09.csv", "18-F-11.csv", "28-S-15.csv", "16-S-11.csv", "9-F-08.csv", "15-F-11.csv", "30-F-15.csv"]

class_acronym = []
course_number_name = []

for x in to_read:
    f = open ("/data/ClassMetrics"+x, "rb")
    read = csv.reader(f, delimiter=",")
    next(reader, None)

    for line in read:
        acronym = line[1]
        if acronym not in class_acronym:
            class_acronym.append(acronym)
        full_name = line[1] + " " + line[2], line[3]
        if full_name not in course_number_name:
            course_number_name.append(full_name)

for x in class_acronym:
    db.session.add(models.Search(name0=x, role="department"))

for x in course_number_name:
    db.session.add(models.Search(name0=x[0], name1=x[1], role="class"))
