from twfy import TWFY
import json
import urllib2

twfy = TWFY.TWFY('B7Ben2G9Zu2kCnRUEwFzJLea')

url = "http://mapit.mysociety.org/areas/SPC"
req = urllib2.Request(url)
constituencies_string = urllib2.urlopen(req).read()

constituencies = json.loads(constituencies_string, 'iso-8859-1')

output = []

for constituency in constituencies.values():
    id =  constituency['id']
    name = constituency['name']

    url = "http://mapit.mysociety.org/area/" + str(id) + ".kml"
    req = urllib2.Request(url)
    polygon = urllib2.urlopen(req).read()

    polygon = polygon[polygon.index("<coordinates>")+13:]
    polygon = polygon[:polygon.index("<")].split(' ')

    polygons = []

    for point in polygon:
        point = point.split(',')[:2]
	points = []

        for p in point:
            p = p.split('.')
            p[1] = p[1][:4]
            points.append(float('.'.join(p)))

        polygons.append(points)


    output.append({"name":name,"id":id,"polygon":polygons})
    print name

fo = open("../data/polygons_clean_floats.js", "w+")
fo.write(json.dumps(output))
fo.close()

print "Done!"
