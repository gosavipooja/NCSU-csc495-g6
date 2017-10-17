#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 11:50:57 2017

@author: michaelkowolenko
"""
from textblob import TextBlob
data = open('/Users/michaelkowolenko/Desktop/test1.TXT').read()
bunch=TextBlob(data)

find_good=bunch.sentences

key_words=['resistance','antibiotics']



for sentence in find_good:
    if(all(map(lambda word: word in sentence, key_words))):
        print(sentence)