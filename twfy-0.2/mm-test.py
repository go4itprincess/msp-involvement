from twfy import TWFY
import json
import re
import codecs
from os.path import isfile
from os import getcwd
import HTMLParser
import random


# ------------------------------------------------------------------------------
#   General helper functions
# ------------------------------------------------------------------------------

def loadFileText(filename):
    f=codecs.open(filename,"rb","utf-8", errors="replace")
    #f=open(filename,"r")

    lines=f.readlines()
    text=u"".join(lines)

##    import unicodedata
##    text = unicodedata.normalize('NFKD', text).decode('UTF-8', 'ignore')

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
    h = HTMLParser.HTMLParser()
    return h.unescape(xmlstr)

def writeTuplesToCSV(columns,tuples,filename):
	"""
	"""
	try:
		f=codecs.open(filename,"wb","utf-8", errors="replace")
	except:
		f=codecs.open(filename+str(random.randint(10,100)),"wb","utf-8", errors="replace")

	line=u"".join([c+u"\t" for c in columns])
	line=line.strip(u"\t")
	line+=u"\n"
	f.write(line)

	pattern=u"".join([u"%s\t" for c in columns])
	pattern=pattern.strip()
	pattern+=u"\n"

	for l in tuples:
		try:
			line=pattern % l
			f.write(line)
		except:
			print "error writing: ", l

	f.close()



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

    while retrieved_rows < all_rows and page <= total_pages:
        try:
            debates=json.loads(twfy.api.getDebates(output='js',type="scotland",person=person_id, num=100, page=str(page)), 'iso-8859-1')
        except:
            print "ERROR downloading data for ", person_id

        if retrieved_rows==0:
            print "Total results: ", debates["info"]["total_results"]
            total_pages=(debates["info"]["total_results"] / debates["info"]["results_per_page"])+1

        retrieved_rows+=debates["info"]["results_per_page"]
        page+=1
        all_rows.extend(debates["rows"])
        print "Added ",debates["info"]["results_per_page"], "rows. Page: ", page-1, "/", total_pages
        if len(debates["rows"])==0:
            break

    debates["rows"]=all_rows
    return debates

def printAllInfoAboutMSP(person_id):
    mp_info=json.loads(twfy.api.getPerson(output='js',id=person_id), 'iso-8859-1')
    mp_info2=json.loads(twfy.api.getMPInfo(output='js',id=person_id, fields=""), 'iso-8859-1')
    print mp_info2, mp_info


def printAllInfoAboutMSPs():
    mp_list = getListOfAllCurrentMSPs()
    results = {}

    for mp in mp_list:
        print mp
        printAllInfoAboutMSP(mp["person_id"])

def getListOfAllCurrentMSPs():
    mp_list = json.loads(twfy.api.getMSPs(output='js',date='01/12/2013'), 'iso-8859-1')

    return mp_list

def saveDebateInterventionsToFile(person_id):
    """
        Does what is says on the tin
    """
    print "Downloading data for person ", person_id
    all_rows=twfyRetrieveAllDebateInterventionsByPerson(person_id)
    print "Download complete, dumping to file:", person_id
    f=open(filenameForPerson(person_id),"wb")
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
    return "\n\n".join([cleanxml(x["body"]) for x in debates["rows"]])


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


def filenameForPerson(person_id):
    return getcwd()+"\\hansard\\"+str(person_id)+".json"

def downloadAllDataForAllMSPs(overwrite=False):
    msps=getListOfAllCurrentMSPs()
    for msp in msps:
        fn=filenameForPerson(msp["person_id"])
        if isfile(fn) and not overwrite:
            print "File for ", msp["person_id"],"already exists"
        if overwrite or not isfile(fn):
            saveDebateInterventionsToFile(msp["person_id"])

def interventionLength1(string):
    """
        Return a number of how long an intervention was, in words.
        Right now it's just the character length divided by 5, theoretically words

    """
    return (len(cleanxml(string)) / 5),

def interventionLength2(string):
    """
        Return a number of how long an intervention was, in words.
        Right now it's just the character length divided by 5, theoretically words

    """
    words=string.split()

    return len(words)

def countMentionsOfConstituency(msp,debate):
    interventions_mentions=0
    total_mentions=0

    for d in debate["rows"]:
        text=cleanxml(d["body"])
        mentions=countMentionsOf(text,msp["constituency"])
        if mentions > 0: interventions_mentions+=1
        total_mentions+=mentions
    return total_mentions,interventions_mentions

def computeMSPStats(msps):
    for msp in msps:
        try:
            debate=loadDebateInterventionsFromFile(filenameForPerson(msp["person_id"]))
        except:
            print "No data downloaded for MSP", msp["name"], " person_id:", msp["person_id"]
            continue

        stats={}
        stats["total_interventions"]=len(debate["rows"])
        stats["avg_intervention_len"]=sum([interventionLength2(r["body"]) for r in debate["rows"]]) / float(stats["total_interventions"])
        text=getTextOfInterventions(debate).lower()
        stats["total_mentions_of_constituency"], stats["interventions_with_mention"]=countMentionsOfConstituency(msp,debate)
        stats["mentions_percentage_of_total_text"]=countMentionsOf(text,msp["constituency"].lower()) / float(interventionLength2(text))
        stats["percentage_of_interventions_with_mention"]=stats["interventions_with_mention"] / float(stats["total_interventions"])
        msp["stats"]=stats

##        info["interventions_with_mentions_of_constituency"]=

##        print msp["name"], "(", msp["constituency"], "), person_id", msp["person_id"]
##        print stats

def countMentionsOf(where, what):
    reg=what.replace(" ", r"\s+?")
    all=[m for m in re.finditer(reg, where, re.IGNORECASE)]
    return len(all)

def compareDownloadedResults():
    msps=getListOfAllCurrentMSPs()
    for msp in msps:
        print msp["person_id"]
        try:
            debates=loadDebateInterventionsFromFile(filenameForPerson(msp["person_id"]))
        except:
            break
        print debates["info"]["total_results"]
        print len(debates["rows"])

def convertInterventionsToText():
    """
        For each MSP in the list, extracts the full text of their interventions
        from the .json, saves it as .txt
    """
    msps=getListOfAllCurrentMSPs()
    for msp in msps:
        fn=filenameForPerson(msp["person_id"])
        if isfile(fn):
            print msp["person_id"]
            fulltext=getTextOfInterventions(loadDebateInterventionsFromFile(fn))
##            fulltext=fulltext.lower()
            writeFileText(fulltext, fn.replace(".json",".txt"))

def saveStatsAsCSV(msps,filename):
    tuples=[]
    for msp in msps:
        if msp.has_key("stats"):
            stats=msp["stats"]
            tuples.append((msp["person_id"],msp["name"],msp["constituency"], msp["party"],
            stats["total_interventions"], stats["avg_intervention_len"], stats["total_mentions_of_constituency"],
            stats["interventions_with_mention"], stats["mentions_percentage_of_total_text"],
            stats["percentage_of_interventions_with_mention"]))

    writeTuplesToCSV("person_id name constituency party total_interventions avg_intervention_len total_mentions_of_constituency interventions_with_mention mentions_percentage_of_total_text percentage_of_interventions_with_mention".split(),tuples,filename)

def main():

    convertInterventionsToText()
##    downloadAllDataForAllMSPs()
##    printAllInfoAboutMSP("14071")
##    print getListOfAllCurrentMSPs()

    msps=getListOfAllCurrentMSPs()
##    writeFileText(json.dumps(msps),"all_msps.json")
##    computeMSPStats(msps)
##    saveStatsAsCSV(msps,"msps_stats.csv")
##    compareDownloadedResults()
    pass

if __name__ == '__main__':
    main()

