import csv
from app import db, models

f = open("Search2.csv", "r", encoding="windows-1252")
f2 = open("Search2mm.csv", "w")
read = csv.reader(f, delimiter=",")
write = csv.writer(f2)
i=0
for line in read:
    if i!=0 and int(line[0]) >= 182 and int(line[0]) < 9692:
        line[4] = line[1].split()[0]
        write.writerow(line)
    else:
        write.writerow(line)
    i+=1

f.close()
f2.close()

f = open("Search2mm.csv", "r", encoding="utf-8")
read = csv.reader(f, delimiter=",")
i=0
for line in read:
    if i !=0:
        db.session.add(models.Search(name0=line[1], name1=line[2], role=line[3], dept=line[4], hits=line[5]))
    i+=1

db.session.commit()
