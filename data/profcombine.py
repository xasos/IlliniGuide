import csv
from fuzzywuzzy import fuzz, process
import time


profs = []
dupes = []
possible_dupes = []
append = []

f = open('professorscleaned2.csv', 'r', encoding='WINDOWS-1252')
read = csv.reader(f, delimiter=',')
i=0
for line in read:
    if i != 0:
        test = ''
        if (line[1] == ''):
            test = line[0].strip() + ' ' + line[2].strip()
        else:
            test = line[0].strip() + ' ' + line[1].strip() + ' ' + line[2].strip()
        profs.append(test)
    i += 1


f = open('professorscleaned2.csv', 'a', encoding='WINDOWS-1252')
write = csv.writer(f)
f2 = open('professors/proflist.csv', 'r', encoding='WINDOWS-1252')
read = csv.reader(f2, delimiter=',')
i=0
for line in read:
    if i != 0:
        test = ''
        global triple
        if (line[8] == ''):
            test = line[6].strip() + ' ' + line[7].strip()
            triple = (line[6].strip(), '', line[7].strip())
        else:
            test = line[6].strip() + ' ' + line[8].strip() + ' ' + line[7].strip()
            middle = line[8].strip()
            if len(line[8]) == 1:
                middle += '.'
            triple = (line[6].strip(), middle, line[7].strip())
        if test in profs:
            dupes.append((test, line[5], triple))
            continue
        if (process.extractOne(test, profs)[1] > 90):

            possible_dupes.append((test, process.extractOne(test, profs)[0], triple))
        else:
            print((test, process.extractOne(test, profs)[0]))
            append.append((test, process.extractOne(test, profs)[0], triple))
    i += 1

print(len(possible_dupes))
print(len(dupes))
print(len(append))

appended = []

for x in append:
    if (x not in appended):
        print(x)
        var = input('decision\n')
        if (var == ''):
            print('written')
            appended.append(x)
            write.writerow([x[2][0], x[2][1], x[2][2]])

for x in possible_dupes:
    if (x not in appended):
        print(x)
        var = input('decision\n')
        if (var != ''):
            print('written')
            appended.append(x)
            write.writerow([x[2][0], x[2][1], x[2][2]])
