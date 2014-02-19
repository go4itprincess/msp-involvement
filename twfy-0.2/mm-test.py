from twfyLib import *


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

