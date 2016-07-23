from app import db, models
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

f = open("data/professors.csv", "rt", encoding="WINDOWS-1252")
f2 = open('data/professorscleaned.csv', 'w')
read = csv.reader(f, delimiter=",")
write = csv.writer(f2)
f3 = open('data/professorsmistakes.csv', 'w')
write2 = csv.writer(f3)
i = 0

search_array=[]

for line in read:
    if i != 0:
        request = urlopen(line[5])
        soup = BeautifulSoup(request, 'html.parser')
        if (line[6] == ''):
            test = line[3] + ' ' +line[4]
        else:
            test = line[3] + ' ' + line[6]+' ' +line[4]
        try:
            name = soup.find('h4', class_='ws-ds-name').string
        except AttributeError:
            write2.writerow([line[3], line[6], line[4]])
        print(test+': ' + name)
        if (test == name):
            write.writerow([line[3], line[6], line[4]])
        else:
            write2.writerow(name.split())
    i += 1
