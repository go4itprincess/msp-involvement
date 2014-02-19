import json
import urllib2
import re

url = "http://mapit.mysociety.org/areas/SPC"
req = urllib2.Request(url)
constituencies_string = urllib2.urlopen(req).read()

constituencies = json.loads(constituencies_string, 'iso-8859-1')

output = []


for constituency in constituencies.values():
    id = constituency['id']
    name = constituency['name']

    url = "http://mapit.mysociety.org/area/" + str(id) + "/geometry"
    req = urllib2.Request(url)

    print(name)
    output.append({'name':name, 'id':id, 'geometry':json.loads(urllib2.urlopen(req).read())})

fo = open("testapp/static/constituencies_geometry.js", "w+")
fo.write(json.dumps(output))
fo.close()

print "Done!"
