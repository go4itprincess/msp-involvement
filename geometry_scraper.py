import json
import urllib2

url = "http://mapit.mysociety.org/areas/SPC"
req = urllib2.Request(url)
constituencies_string = urllib2.urlopen(req).read()

constituencies = json.loads(constituencies_string, 'iso-8859-1')

output = []
fo = open("data/population.csv", "r")
population = fo.read()
fo.close()

population = population.split('\n')
pops = []
for p in population:
    p = p.split(',')
    pops.append(p)

for constituency in constituencies.values():
    id = constituency['id']
    name = constituency['name']

    url = "http://mapit.mysociety.org/area/" + str(id) + "/geometry"
    req = urllib2.Request(url)
    geometry = json.loads(urllib2.urlopen(req).read())

    url = "http://mapit.mysociety.org/area/" + str(id)
    req = urllib2.Request(url)
    code = json.loads(urllib2.urlopen(req).read())

    pop = 0

    for p in pops:
        if str(code['codes']['gss']) == p[0]:
            pop = int(p[1])
            break


    print name
    output.append({'name':name, 'id':id, 'geometry': geometry, 'gss': code['codes']['gss'], 'population': pop})

fo = open("testapp/static/constituencies_geometry.js", "w+")
fo.write(json.dumps(output))
fo.close()

print "Done!"
