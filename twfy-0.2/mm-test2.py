#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      MasterMan
#
# Created:     19/02/2014
# Copyright:   (c) MasterMan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from twfyLib import *

import glob
import os
import codecs
import math
import cPickle

from string import punctuation
from nltk import word_tokenize

stopwords=['the', 'of', 'a', 'at', 'an']
stopwords.extend(punctuation)

msps_constituencies=[25114, 25104, 14115, 10525, 25112, 14071, 13969, 13976, 25081, 14089, 14091, 14102, 13993, 14013, 13961, 14075, 13966, 14099, 14009, 13994, 25078, 13949, 14070, 14085, 13987, 25207, 13982, 14002, 25098, 25075, 14031, 10102, 25095, 25084, 25092, 14026, 25094, 14043, 13985, 14024, 25082, 14117, 13984, 14025, 14039, 25101, 14105, 14061, 14056, 13980, 13968, 25115, 14012, 14041, 25074, 14000, 14029, 25110, 13947, 25079, 14046, 25072, 10581, 10148, 25096, 14008, 14022, 14092, 14107, 13971, 14057, 14059]

def tokenizeText(text):
    """
        Abstracts over how the tokenizing is actually done
    """
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in punctuation and t not in stopwords]
    return tokens

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

def bow2counts(bow):
	"""
		Returns a dictionary of [word]=count from BOW list
	"""
	counts={}
	for token in bow:
		counts[token]=counts.get(token,0)+1
	return counts


class mmtfidf:
    """
        MasterMan's TFIDF implementation, code from Text Technologies
    """
    def __init__(self,all_docs):
        self.documents=all_docs
        self.qry={}
        self.docNum=0
        self.docFrequency={}    # how many documents the word appears in
        self.docLen={}          # the length of each document
        self.avgdoclen=0        # the mean word length of all documents
        self.sEx={}             # a dictionary of SoundEx codes and all the words that fit them in the document
        self.synonyms={}        # a nested dictionary of coocurring words and the number of such occurrences
        self.seenAlone={}       # how many times a word was seen through the whole collection of docs
        self.seenTogether={}
        self.dice={}            # a dictionary of coocurring words and their Dice coefficient

        self.konst=2.0          # fancy constant for TFIDF formula

        self.loadDocs()
        self.buildMatrix()

    def loadDocs(self):
        """
            Adds "counts" to the document dict, which is the BOW proper
            also adds "len" which is the total length of the document
        """
        tlen=0

        for doc in self.documents:
            doc["len"]=len(doc["BOW"])       # document length = number of total words in bag-of-words list
            tlen+=doc["len"]
            doc["counts"]=self.bow2counts(doc["BOW"])

        self.docNum=len(self.documents)
        self.avgdoclen=tlen/self.docNum if self.docNum!=0 else 0

    def buildMatrix(self):
        for doc in self.documents:
            for w in doc["counts"]:
                self.docFrequency[w]=self.docFrequency.get(w,0)+1
                self.seenAlone[w]=self.seenAlone.get(w,0) + doc["counts"][w]

    def bow2counts(self,bow):
        """
            Returns a dictionary of [word]=count from BOW list
        """
        counts={}
        for token in bow:
            counts[token]=counts.get(token,0)+1
        return counts

    def wordScore(self, w, doc):
        vec=doc["vec"]
        score=(vec[w]/(vec[w]+((self.konst*doc["len"])/self.avgdoclen)))*math.log(float(self.docNum)/self.docFrequency.get(w,0.000000001),2)
        return score

    def runQuery(self, query):
        text=''

        scores=[]
        for doc in self.documents:     # for every document
            score=0
            dvalues=doc["counts"]   # dictionary of [unique words in the document] = their count

            for w in query.keys():  # for every term in the query
                tmp=dvalues.get(w)
                if tmp:
                    tfq=query[w]
                    tfd=tmp
                    score+=tfq*(tfd/(tfd+((self.konst*doc["len"])/self.avgdoclen)))*math.log(float(self.docNum)/self.docFrequency.get(w,0),2)
            scores.append((score,doc))

        results=sorted(scores, key=lambda x:x[0], reverse=True)

##        for key, value in sorted(sqd.iteritems(), key=lambda (k,v): (v,k), reverse=True):
##            if value > 0:
##                s= "%0.6f" % value
##                text+=str(q)+'\t0\t'+ str(key)+'\t0\t  ' + s + '\t0\n'
        return results

def loadTextDocs(dir):
    all_docs=[]
    all_speakers=[]

##    for fn in glob.glob(dir+"*.txt"):
    for msp in msps_constituencies:
        fn=dir+str(msp)+".txt"
        print "Loading ", fn
        f=codecs.open(fn,"rb","utf-8", errors="replace")
        lines=f.readlines()

        bow=tokenizeText(" ".join(lines))
        vec=bow2counts(bow)
        all_speakers.append({"person_id":os.path.basename(fn).replace(".txt",""),
        "vec":vec,"len":len(bow)})

        for line in lines:
            line=line.strip().lower()
            if len(line) > 0:
                #print line
                tokens=tokenizeText(line)
                #line= [t for t in tokens if t not in punctuation and t not in stopwords]
                doc={"BOW":tokens}
                all_docs.append(doc)
    return all_docs, all_speakers


def main():

    MAX_WORDS=50
    all_docs, all_speakers=loadTextDocs(os.getcwd()+"\\hansard\\")
    mm=mmtfidf(all_docs)
    saveObject("tfidfmodel.pic",mm)
    saveObject("all_speakers.pic",all_speakers)

##    mm=loadObject("tfidfmodel.pic")
##    all_speakers=loadObject("all_speakers.pic")

    for person in all_speakers:
        print "Processing chatter for",person["person_id"]
        person["tokens"]=tokenizeText(person["text"].lower())
        person["word_scores"]={}
        for word in person["tokens"]:
            score=mm.wordScore(word,doc)
            person["word_scores"][score]=word

            person["top_words"]=[(word,score) for word,score in sorted(person["word_scores"].iteritems(),key=lambda x:x[0], reverse=True)[:MAX_WORDS]]
        print person["person_id"]
        print person["top_words"]


if __name__ == '__main__':
    main()
