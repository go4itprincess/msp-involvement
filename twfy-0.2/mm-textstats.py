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


vectorizer = CountVectorizer(min_df=1, stop_words="english")

from sklearn.feature_extraction.text import TfidfVectorizer

content = ["Bursting the Big Data bubble starts with appreciating certain nuances about its products and patterns","the real solutions that are useful in dealing with Big Data will be needed and in demand even if the notion of Big Data falls from the height of its hype into the trough of disappointment"]


c1=["one one one one one two two three"]
c2=["one two three three"]

##self.tfidf_vectorizer = TfidfVectorizer(decode_error="replace", preprocessor=lambda x:x, tokenizer=lambda x:[y for y in x])
##self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.all_bows)

tfidf_vectorizer = TfidfVectorizer(decode_error="replace")

a = tfidf_vectorizer.fit_transform(c1)
b = tfidf_vectorizer.fit_transform(c2)



print(x)

def main():
    pass

if __name__ == '__main__':
    main()
