from twfy import TWFY
import json
import urllib2

twfy = TWFY.TWFY('B7Ben2G9Zu2kCnRUEwFzJLea')

url = "http://mapit.mysociety.org/areas/SPC"
req = urllib2.Request(url)
constituencies_string = urllib2.urlopen(req).read()

constituencies = json.loads(constituencies_string, 'iso-8859-1')

for constituency in constituencies.values():
    id =  constituency['id']
    name = constituency['name']

    url = "http://mapit.mysociety.org/area/" + str(id) + ".kml"
    req = urllib2.Request(url)
    polygon = urllib2.urlopen(req).read()

    try:
        fo = open("polygons_Scotland/" + name + ".kml", "w+")
        fo.write(polygon)
        fo.close()
    except:
        print "Ouch"

print "Done!"
