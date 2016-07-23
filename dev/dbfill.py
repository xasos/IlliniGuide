from app import db, models
import csv, glob

holder = []
long_name=[]
course_number_name = []

for filename in glob.glob('data/ClassMetrics/*.csv'):
    f = open(filename, "rt", encoding="WINDOWS-1252")
    read = csv.reader(f, delimiter=",")
    i = 0

    for line in read:
        if i != 0:
            full_name = [line[1] + " " + line[2], line[3], line[1]]
            if full_name not in course_number_name:
                course_number_name.append(full_name)
        i += 1

f = open("dev/fixer.csv", "rt", encoding="WINDOWS-1252")
read = csv.reader(f, delimiter=",")

i=0
for line in read:
    if i !=0:
        db.session.add(models.Search(name0=line[1], name1=line[2], role=line[3], dept=line[4], hits=int(line[5])))
    i+=1

for x in course_number_name:
    db.session.add(models.Search(name0=x[0], name1=x[1], role="class", dept=x[2]))

db.session.commit()
