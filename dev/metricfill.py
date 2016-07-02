from app import db, models
import glob, csv

for filename in glob.glob("data/ClassMetrics/*.csv"):
    f = open(filename, "r", encoding="windows-1252")
    read = csv.reader(f, delimiter=',')
    i = 0
    for line in read:
        if i != 0:
            db.session.add(models.Metrics(subject=line[1], number=line[2], title=line[3], section=line[4], term=line[5],
                            instructor=line[7], aplus=line[8], a=line[9], aminus=line[10], bplus=line[11], b=line[12], bminus=line[13],
                            cplus=line[14], c=line[15], cminus=line[16], dplus=line[17], d=line[18], dminus=line[19], f=line[20],
                            w=line[21], avg=line[22]))
        i += 1

db.session.commit()
