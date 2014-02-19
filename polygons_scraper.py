import json
import urllib2
import re

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

    url = "http://mapit.mysociety.org/area/" + str(id) + ".kml"
    req = urllib2.Request(url)

    polygons_scraped = re.findall("<coordinates>(.+?)</coordinates>",urllib2.urlopen(req).read())
    polygons = []

    url = "http://mapit.mysociety.org/area/" + str(id)
    req = urllib2.Request(url)
    code = json.loads(urllib2.urlopen(req).read())

    pop = 0
    for p in pops:
        if str(code['codes']['gss']) == p[0]:
            pop = int(p[1])
            break


    for poly in polygons_scraped:
        coordinates = poly.split(' ')

        polygon = []
        i = 0

        for coordinate in coordinates:
            coordinate = map(float,coordinate.split(',')[:2])
            coordinate[0], coordinate[1] = coordinate[1], coordinate[0]

            if i%10 == 0:
                polygon.append(coordinate)
            i += 1

        polygons.append(polygon)

    output.append({"name":name,"id":id,"polygon":polygons, 'population': pop})
    print name

fo = open("testapp/static/constituencies_polygons.js", "w+")
fo.write(json.dumps(output))
fo.close()

print "Done!"
