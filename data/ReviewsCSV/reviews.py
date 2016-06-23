import urllib, json, os, math

professorlist = []
for i in range(1, 197):
    url="http://www.ratemyprofessors.com/find/professor/?department=&institution=University+Of+Illinois+at+Urbana-Champaign&page="+str(i)+"&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=1112&sortBy="
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    for x in data["professors"]:
        professorlist.append({"First":x["tFname"], "Last":x["tLname"], "tid":x["tid"], "numRatings":x["tNumRatings"]})

print("complete")
print(len(professorlist))
#for x in professorlist:
#    print(x)

for y in professorlist:
    if (y["numRatings"] <= 3 and y["tid"] != 1401586 and y["tid"] != 1493506 and y['tid'] != 1661512 and y["tid"] != 1664593 and y["tid"] != 1620131):

        for i in range(1,(int(math.ceil(y["numRatings"]/20)+2))):
            url="http://www.ratemyprofessors.com/paginate/professors/ratings?tid="+str(y["tid"])+"&page="+str(i)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            name = y["First"].replace(" ", "") + "_" + y["Last"].replace(" ", "") + "_" + str(i) + "_" + "reviews."

            with open(name+"json", "w") as outfile:
                json.dump(data, outfile, sort_keys = True, indent = 4)
            os.system("in2csv " + name + "json > "+name+"csv -k ratings" )
