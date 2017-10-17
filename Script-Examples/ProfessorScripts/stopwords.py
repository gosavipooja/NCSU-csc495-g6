#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:53:23 2017

@author: michaelkowolenko
"""

import sys
import io
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

data = open('/Users/michaelkowolenko/Desktop/class/test.txt', encoding='utf-8').read()

words = word_tokenize(data)
words_selected = []
for w in words:
    if w not in stop_words:
        words_selected.append(w)


with open('/Users/michaelkowolenko/Desktop/test1.txt', 'w', encoding='utf-8') as f:
    print(words, file=f)

#   print(words_selected)
#print(words)

#apply stats to words selected