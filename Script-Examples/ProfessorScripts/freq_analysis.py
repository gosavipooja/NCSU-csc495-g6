#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:10:33 2017

@author: michaelkowolenko
"""

import sys
import io
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
#open the file

data = open('/Users/michaelkowolenko/Desktop/class/test.txt', encoding='utf-8').read()

#print(data) - just a test

words = word_tokenize(data)

spread=nltk.FreqDist(words)
spread.plot(50,cumulative=True)
for word, frequency in spread.most_common(100):
    print(u'{};{}'.format(word, frequency))
    
    