import urllib2

#fast and ugly python code...

url = "http://www.scottish.parliament.uk/msps/177.aspx"
req = urllib2.Request(url)
source = urllib2.urlopen(req).read()

current_msp = ""

while (len(source) > 0):
	if "<a href=\"/msps/currentmsps/" in source:
		source = source[source.index("<a href=\"/msps/currentmsps/"):]
		source = source[source.index("<strong>") + 58:]
		
		name = source[:source.index("</strong>")].replace('\n','').replace('\t','')

		source = source[source.index("src=") + 5:]
		image = "http://www.scottish.parliament.uk" + source[:source.index("\"")]
		

		source = source[source.index("<p>") + 24:]
		party = source[:source.index("</p>")].replace('\n','').replace('\t','')
		
		source = source[source.index("<strong>") + 44:]
		constituencies = source[:source.index("</strong>")].replace(" and ", ";").replace('\n','').replace('\t','')

		current_msp += name + ";" + party + ";" + constituencies + ";" + image + "\n"

	else:
		break;

fo = open("current_msps.csv", "w+")
fo.write(current_msp)
fo.close()

print "Done!"
