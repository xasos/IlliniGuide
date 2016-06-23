import urllib, json, os, math

professorlist = []
for i in range(1, 197):
    url="http://www.ratemyprofessors.com/find/professor/?department=&institution=University+Of+Illinois+at+Urbana-Champaign&page="+str(i)+"&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=1112&sortBy="
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    name = "proflist" + str(i)
    with open(name+'.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 4)
    os.system("in2csv " + name + ".json > "+name+".csv -k professors" )
