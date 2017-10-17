import os
import operator
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

def dump_keys(d, lvl=0):
    for k, v in d.items():
        spacing = lvl * ' '
        key = '{:15}'.format(str(k))
        value = ' - ' + str(v)
        print( spacing + key + value)
        if type(v) == dict:
            dump_keys(v, lvl+1)

tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')

# open the file
repo_dir = Path(__file__).resolve().parents[1]
with open(os.path.join(repo_dir, "input/Hospital-Ranking/hospital-ranking.TXT"), encoding='utf-8') as data:
    words = word_tokenize(data.read())

vectorizer = TfidfVectorizer(min_df=1)
X = vectorizer.fit_transform(words)
idf = vectorizer.idf_

# Get dictionary
my_dict = dict(zip(vectorizer.get_feature_names(), idf))
# Sort it from most value to least
my_dict = dict(sorted(my_dict.items(), key=operator.itemgetter(1)))
# Print the dictionary
dump_keys(my_dict)