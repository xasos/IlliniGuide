import csv, glob

with open("proflist.csv", "a") as writefile:
    writer = csv.writer(writefile)
    for filename in glob.glob('csv/*.csv'):
        f = open(filename, "r")
        read = csv.reader(f, delimiter=",")
        i = 0
        for line in read:
            if i != 0:
                writer.writerow(line)
            i += 1
