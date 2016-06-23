import urllib, json
for i in range(1, 197):
     url="http://www.ratemyprofessors.com/find/professor/?department=&institution=University+Of+Illinois+at+Urbana-Champaign&page="+str(i)+"&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=1112&sortBy="
     response = urllib.urlopen(url)
     data = json.loads(response.read())
     with open('data.txt', 'a') as outfile:
          json.dump(data, outfile, sort_keys = True, indent = 4)
