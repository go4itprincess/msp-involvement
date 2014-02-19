import json
import urllib2

url = "http://mapit.mysociety.org/areas/SPC"
req = urllib2.Request(url)
constituencies_string = urllib2.urlopen(req).read()

constituencies = json.loads(constituencies_string, 'iso-8859-1')

output = []


for constituency in constituencies.values():
    id = constituency['id']
    name = constituency['name']

    url = "http://mapit.mysociety.org/area/" + str(id)
    req = urllib2.Request(url)


    print(name)
    output.append(json.loads(urllib2.urlopen(req).read()))

fo = open("testapp/static/constituencies_gss.js", "w+")
fo.write(json.dumps(output))
fo.close()

print "Done!"
