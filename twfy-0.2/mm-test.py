'''
An example that uses the python interface to the TWFY API(http://www.theyworkforyou.com/api/)

   This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from twfy import TWFY
import json

# ------------------------------------------------------------------------------
#   General helper functions
# ------------------------------------------------------------------------------

def loadFileText(filename):
	f=codecs.open(filename,"rb","utf-8", errors="replace")
	#f=open(filename,"r")

	lines=f.readlines()
	text=u"".join(lines)

##	import unicodedata
##	text = unicodedata.normalize('NFKD', text).decode('UTF-8', 'ignore')

	f.close()
	return text

def writeFileText(text,filename):
	f2=codecs.open(filename,"w","utf-8",errors="replace")
	f2.write(text)
	f2.close()

def cleanxml(xmlstr):
    """
        Removes all XML/HTML tags
    """
    xmlstr=re.sub(r"</?.+?>"," ",xmlstr)
    xmlstr=xmlstr.replace("  "," ").strip()
    return xmlstr


twfy = TWFY.TWFY('B7Ben2G9Zu2kCnRUEwFzJLea')
#Get list of all MPs
#A date between '01/05/1997' and todays date.

##boundary=json.loads(twfy.api.getGeometry(output="js",name="East Lothian"), 'iso-8859-1')
##print boundary

##debates=json.loads(twfy.api.getDebates(output="js",name="East Lothian"), 'iso-8859-1')

def twfyRetrieveAllDebateInterventionsByPerson(person_id):
    """
        This function cals the TWFY getDebates API function repeatedly, collating all interventions
        of an MSP referred by their person_id

        Returns a dict with all the info collated. ["rows"] in that dict contains the actual interventions

    """

    retrieved_rows=0
    num_rows=9999999
    all_rows=[]
    page=1
    total_pages=999999999

    while retrieved_rows < all_rows and page < total_pages:
        debates=json.loads(twfy.api.getDebates(output='js',type="scotland",person=person_id, page=str(page)), 'iso-8859-1')

        if retrieved_rows==0:
            print "Total results: ", debates["info"]["total_results"]
            total_pages=debates["info"]["total_results"] / debates["info"]["results_per_page"]

        retrieved_rows+=debates["info"]["results_per_page"]
        page+=1
        all_rows.extend(debates["rows"])
        print "Added ",debates["info"]["results_per_page"], "rows. Page: ", page, "/", total_pages
        if len(debates["rows"])==0:
            break

    debates["rows"]=all_rows
    return debates

def printAllInfoAboutMSPs():
    mp_list = getListOfAllCurrentMSPs()
    results = {}

    for mp in mp_list[:1]:
        print mp
        mp_info=json.loads(twfy.api.getPerson(output='js',id=mp["person_id"]), 'iso-8859-1')
        mp_info2=json.loads(twfy.api.getMPInfo(output='js',id=mp["person_id"], fields=""), 'iso-8859-1')
        print mp_info2, mp_info

def getListOfAllCurrentMSPs():
    mp_list = json.loads(twfy.api.getMSPs(output='js',date='01/12/2013'), 'iso-8859-1')

    return mp_list

def saveDebateInterventionsToFile(person_id):
    """
        Does what is says on the tin
    """
    all_rows=twfyRetrieveAllDebateInterventionsByPerson("14071")
    print "Download complete, dumping to file:", person_id
    f=open(str(person_id)+".json","wb")
    json.dump(all_rows,f)
    f.close()

def loadDebateInterventionsFromFile(filename):
    f=open(filename,"rb")
    debates=json.load(f)
    return debates


def getTextOfInterventions(debates):
    """
        Just returns a massive string of everything the poor bastard said
    """
    return " ".join([cleanxml(x) for x in debates["rows"]])


##saveDebateInterventionsToFile("14071")


##printAllCurrentMSPs()

def countMSPsForEachParty():
    """
        Count the number of MPs for each party.
    """

    for mp in mp_list:
        print mp
        party =  mp['party']
        if party in results.keys():
            results[party] += 1
        else:
            results[party] = 1

    total_seats = float(sum(results.values()))

    #Print the results.
    for k, v in results.iteritems():
        print k, ' = ', (v/total_seats)*100, '%'



def downloadAllDataForAllMSPs():
    msps=getListOfAllCurrentMSPs()
    for msp in msps:
        saveDebateInterventionsToFile(msp["person_id"])

def printHowMuchTheyAllSpoke():


def main():

    debates=loadDebateInterventionsFromFile("14071.json")
    print debates["info"]["total_results"]

    pass

if __name__ == '__main__':
    main()

