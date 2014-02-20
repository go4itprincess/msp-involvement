import json
import urllib2
import re
import geojson

url = "http://mapit.mysociety.org/areas/SPC"
req = urllib2.Request(url)
constituencies_string = urllib2.urlopen(req).read()
constituencies = json.loads(constituencies_string, 'iso-8859-1')

output = []
fo = open("data/population.csv", "r")
population = fo.read()
fo.close()

url = "http://ilwhack.modulo.ee/stats"
req = urllib2.Request(url)
stats = json.loads(urllib2.urlopen(req).read())
stats = stats['result']


def extract(name):
    for c in stats:
        if c['c_name'] == name:
            return {
                'rank_gen': c["rank_gen"],
                'rank_cri': c["rank_cri"],
                'rank_ed': c["rank_ed"],
                'rank_emp': c["rank_emp"],
                'rank_geo': c["rank_geo"],
                'rank_hea': c["rank_hea"],
                'rank_hou': c["rank_hou"],
                'rank_inc': c["rank_inc"]
            }
    print "extract fails at: " + name
    raise BaseException("Fuck me!")

population = population.split('\n')
pops = []
for p in population:
    p = p.split(',')
    pops.append(p)

feature_list = []
for constituency in constituencies.values():
    id = constituency['id']
    name = constituency['name']

    url = "http://mapit.mysociety.org/area/" + str(id) + ".kml"
    req = urllib2.Request(url)

    polygons_scraped = re.findall("<coordinates>(.+?)</coordinates>", urllib2.urlopen(req).read())
    polygons = []

    url = "http://mapit.mysociety.org/area/" + str(id)
    req = urllib2.Request(url)
    code = json.loads(urllib2.urlopen(req).read())

    pop = 0
    for p in pops:
        if str(code['codes']['gss']) == p[0]:
            pop = int(p[1])
            break

    pointsList = []
    print name
    for poly in polygons_scraped:
        coordinates = poly.split(' ')

        i = 0
        points = []
        for coordinate in coordinates:
            coordinate = map(float,coordinate.split(',')[:2])

            if i%10 == 0:
                point = [coordinate[0], coordinate[1]]
                points.append(point)
            i += 1
        pointsList.append([points])
    multipolygon = geojson.MultiPolygon(coordinates=pointsList)
    feature = geojson.Feature(id=id, geometry=multipolygon, properties={'population': pop, 'name': name, 'ranks': extract(name)})
    feature_list.append(feature)
feature_collection = geojson.FeatureCollection(features=feature_list)

fo = open("testapp/static/constituencies_geojson.js", "w+")
fo.write("var constituencies = " + geojson.dumps(feature_collection))
fo.close()

print "Done!"
