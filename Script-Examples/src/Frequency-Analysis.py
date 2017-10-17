"""
@author: tdortiz
"""

import os
import sys
import io
import nltk
import string
from pathlib import Path
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

repo_dir = Path(__file__).resolve().parents[1]

# Create stop words
stop_words            = set(stopwords.words('english')) | set(string.punctuation)
stop_words_economic   = {'it', '\'s', '--', '\'\'', 'For', 'As', 'physicians', 'Alex', 'NNY'}
stop_words_technical  = {'it','technical','Technical','per','12','this','including','rights','reserved','US','2015','all','years','also','we','was','not','care','as','he','documents','more','','have','from','their','has','will','be','said','s','at','(',')','are','by','on','``','','"','with','as','that','is','for','all','in','to','of','and','the','.',':','*','`','2016','been','one','who','our','its','about','i','or','can','but',';','-','`','a','an','such','http','were','there','other','major','which','they','1000','copyright','words','new','may','well','his','next','into','$','&','--','some','had','up','than','key','would','do','over'}
stop_words_legal      = {'it', '\'s', '--', '\'\'', 'For', 'As', 'the', 'The','All',',','\'','\"','hospital','Hospital','legal','said','also','patient','would','But','could'}
stop_words_ethical    = {'In','It','If','Pg','1','n\'t','See','A','Ethics','patients','997','must','says','Dr.','doctors','ethical','Ethical','ethics','medical','health','make','need','Health'}
stop_words_procedural = {'Royal', 'two', 'TEE', 'year', 'B.C', 'St.', 'even' }
stop_words_political  = {'This', 'hospitals', 'He', 'state', 'years', 'last', 'No', 'Dr', 'staff', 'one', 'We', 'I', 'local'}
    
# add all stop words together
stop_words |= stop_words_economic | stop_words_technical | stop_words_legal | stop_words_ethical | stop_words_procedural | stop_words_political

# open the file
data = open(os.path.join(repo_dir, "input/Hospital-Technical/Company_Profiles_and_Directories_US_Law_Revi2017-08-31_01-25.TXT"), encoding='utf-8').read()

# Select words if they're not in the stop list
words = word_tokenize(data)
words_selected = []
for w in words:
    if w not in stop_words:
        words_selected.append(w)

# Plot the graph
spread = nltk.FreqDist(words_selected)
spread.plot(50, cumulative=True)

# Print the word - frequency
for word, frequency in spread.most_common(100):
    print(u'{} - {}'.format(word, frequency))
