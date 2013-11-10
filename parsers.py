#!/usr/bin/env python

from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
import nltk

def stem(s):
    """
        return stemmed string
    """
    d = word_tokenize(s)
    s = nltk.PorterStemmer()
    d = [s.stem(w.lower()) for w in d]
    return " ".join(d)
