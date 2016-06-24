from app import db, models
import csv, glob

def addspace(coursecode):
    y=0
    for x in coursecode:
        if x.isdecimal():
            break
        y+=1
    return coursecode[0:y] + " " + coursecode[y:]

for filename in glob.glob('data/ReviewsCSV/CSV\'s/*.csv'):
    print(filename)
    f = open(filename, "r")
    read = csv.reader(f, delimiter=",")
    i = 0
    for line in read:
        if i != 0:
            name = filename.split("/")[3].split("_")[0]+ " " + filename.split("/")[3].split("_")[1]
            db.session.add(models.Reviews(professorname= name, classname=addspace(line[10]), comments=line[11], date=line[12], quality=float(line[18]), easy=float(line[13])))
        i += 1

db.session.commit()
