#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      MasterMan
#
# Created:     18/02/2014
# Copyright:   (c) MasterMan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from __future__ import division, unicode_literals

from sklearn.feature_extraction.text import CountVectorizer

import numpy as np
import os
import codecs
import re
import glob
import json

vectorizer = CountVectorizer(min_df=1, stop_words="english")

from sklearn.feature_extraction.text import TfidfVectorizer


msps_constituencies=[25114, 25104, 14115, 10525, 25112, 14071, 13969, 13976, 25081, 14089, 14091, 14102, 13993, 14013, 13961, 14075, 13966, 14099, 14009, 13994, 25078, 13949, 14070, 14085, 13987, 25207, 13982, 14002, 25098, 25075, 14031, 10102, 25095, 25084, 25092, 14026, 25094, 14043, 13985, 14024, 25082, 14117, 13984, 14025, 14039, 25101, 14105, 14061, 14056, 13980, 13968, 25115, 14012, 14041, 25074, 14000, 14029, 25110, 13947, 25079, 14046, 25072, 10581, 10148, 25096, 14008, 14022, 14092, 14107, 13971, 14057, 14059]


STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fify", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"
    ,"scotland", "scottish", "people", "member", "members", "said",
    "government", "committee", "important", "know", "way", "ensure", "years",
    "legislation", "amendment", "think", "million", "report",
    "minister","law", "bill", "believe", "welcome", "fact", "simply", "want",
    "000","00","cent", "make", "point", "mr", "number", "ask", "parliamentary", "like",
    "does", "do", "time", "say", "secretary", "parliament", "cabinet", "need",
    "things", "right", "new", "place", "heard", "good", "evidence","ms", "come",
    "great", "going", "huge", "just", "look", "say", "best", "case", "long", "let",
    "talked", "thank", "sure", "issue", "benefit", "better", "recent", "aware",
    "difficult", "recognise", "taken", "use", "speech", "hope", "result", "debate",
    "matter", "administration", "person", "programme", "agree", "consider", "particular",
    "deal", "level", "sure", "understand", "court", "clear", "did", "act", "cases", "set",
    "provide", "strategy", "looked", "importance", "day", "chamber", "process", "course",
    "year", "referred", "issues", "working", "authorities", "waiting", "plan", "pay"
    "issued", "backed", "freeze", "run", "attack", "13", "2007",
    "heard","making", "ashamed", "opposition", "told", "comes", "leader", "happened",
    "present", "consultation", "terminology", "confusion", "amendments", "regularly",
    "chair", "finding", "links", "realise", "directly", "potential", "party", "parties", "means",
    "lot", "noted", "increasingly", "living", "seen", "hear", "priorities", "ignoring",
    "imposing", "licensing", "john", "despite", "created", "sees", "continuing",
    "chances", "concentrate", "agreed", "question", "explicitly", "showed", "range",
    "including", "excluding", "short", "long", "afternoon", "morning", "night",
    "pointed", "effect", "certain", "approach", "listing", "rapidly", "slowly",
    "appearing", "commits", "intent", "existence", "spuriously"
     ])


def saveObject(filename, obj):
	"""
		Pickle an object
	"""
	f=open(filename,"wb")
	cPickle.dump(obj,f)
	f.close()

def loadObject(filename):
	"""
		Load the saved (pickled) object from file
	"""
	f=open(filename,"rb")
	object=cPickle.load(f)
	return object

def loadTextDocs(dir):
    MAX_WORDS=50
    tfidf_vectorizer = TfidfVectorizer(decode_error="replace", stop_words=STOP_WORDS)

    all_speakers=[]

    for fn in glob.glob(dir+"*.txt"):
##    for msp in msps_constituencies[:50]:
##        fn=dir+str(msp)+".txt"
        print "Loading ", fn
        f=codecs.open(fn,"rb","utf-8", errors="replace")
        lines2=[]
        lines=f.readlines()
        for l in lines:
            lines2.append(re.sub(r"\d+(m|gwh|km)?.\s?"," ",l,0,re.IGNORECASE))
        f.close()
        vec = tfidf_vectorizer.fit_transform(lines2)
##        vec = tfidf_vectorizer.fit_transform([" ".join(lines2)])

    for fn in glob.glob(dir+"*.txt"):
##    for msp in msps_constituencies[:50]:
##        fn=dir+str(msp)+".txt"
        print "Loading ", fn
        f=codecs.open(fn,"rb","utf-8", errors="replace")
        lines2=[]
        lines=f.readlines()
        for l in lines:
            lines2.append(re.sub(r"\d+(m|gwh|km)?.\s?"," ",l,0,re.IGNORECASE))
        f.close()
        vec = tfidf_vectorizer.fit_transform(lines2).toarray().ravel()
##        vec = tfidf_vectorizer.fit_transform([" ".join(lines2)]).toarray().ravel()

        names=np.array(tfidf_vectorizer.get_feature_names())
        scores=zip(names,vec)
        scores=sorted(scores,key=lambda x:x[1],reverse=True)[:MAX_WORDS]
        filtered=[]

        for word, score in scores:
            if score > 0:
                filtered.append((word,score))

        for word, score in filtered:
            print unicode(word),score

        speaker={"person_id":os.path.basename(fn).replace(".txt",""),"top_words":filtered}
        all_speakers.append(speaker)

    f=open("all_msps.json","rb")
    persons=json.load(f)
    f.close()

    for i in range(len(all_speakers)):
        for f in range(len(persons)):
            if all_speakers[i]["person_id"] == persons[f]["person_id"]:
                all_speakers[i]["constituency"]=persons[f]["constituency"]
                all_speakers[i]["name"]=persons[f]["name"]

    f=open("msps_words.json","wb")
    json.dump(all_speakers,f)
    f.close()

    pass


def main():
    loadTextDocs(os.getcwd()+"\\hansard\\")

if __name__ == '__main__':
    main()
