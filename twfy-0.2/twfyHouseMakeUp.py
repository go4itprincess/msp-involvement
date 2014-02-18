from twfy import TWFY
import json
import urllib2

twfy = TWFY.TWFY('B7Ben2G9Zu2kCnRUEwFzJLea')

constituencies = json.loads(twfy.api.getConstituencies(output='js',date='05/05/2012'), 'iso-8859-1')

for constituency in constituencies:
    name =  constituency['name']

    url = "http://www.theyworkforyou.com/api/getBoundary?key=B7Ben2G9Zu2kCnRUEwFzJLea&name=" + name
    req = urllib2.Request(url)
    polygon = urllib2.urlopen(req).read()

    try:
        fo = open("polygons/" + name + ".kml", "w+")
        fo.write(polygon)
        fo.close()
    except:
        print "Ouch"

print "Done!"
