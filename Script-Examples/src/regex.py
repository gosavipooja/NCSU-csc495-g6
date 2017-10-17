import os
from pathlib import Path
import re
from textblob import TextBlob

# Open input file
repo_dir = Path(__file__).resolve().parents[1]
data = open(os.path.join(repo_dir, "input/Hospital-Ranking/hospital-ranking.TXT"), encoding='utf-8').read()
bunch=TextBlob(data)
all_sentences=bunch.sentences

# Create key words
key_words            = set()
key_words_economic   = {'$', 'dollar', 'tax', 'taxes', 'job', 'jobs', 'economic', 'economy', 'employ', 
                        'financial', 'growth', 'finance', 'affordable', 'cheap', 'inexpensive', 'cost-effective', 
                        'cost-efficient', 'sustainable', 'fiscal', 'payroll', 'finance', 'price', 'cost', 'fine', 
                        'cutback', 'money', 'wage', 'salary'}
key_words_technical  = {'recent','annualized','extraordinary','trailing','fiscal','quarter','EPS','Margin'
                        'shares','income','change','TTM'}
key_words_legal      = {'patients','health','documents','medical','court','children','reserved','publication',
                        'newspaper','doctors','rights','government','news','language','services'}
key_words_ethical    = {'committee','University','LANGUAGE','DOCUMENTS','Reserved','Catholic','treatments',
                        'issues','Copyright','practice','consent','Professionals'}
key_words_procedural = {'procedure', 'policy', 'scheme', 'measure', 'process', 'action', 'operation',
                        'ways', 'rules', 'mechanism', 'proceeding', 'practice', 'progress', 'step', 'fast', 'efficiency'}
key_words_political  = {'government', 'public', 'rights', 'newpaper', 'byline', 'Minister', 'load-data', 'copyright',
                         'service', 'private'}

# add all key words together
key_words |= key_words_economic | key_words_technical | key_words_legal | key_words_ethical | key_words_procedural | key_words_political

# Setup Regex
regex = r'(.*)[$](.*)'
pattern = re.compile(regex)

sent_num = 0
for sentence in all_sentences:
    if(any(map(lambda word: word in sentence, key_words))):
    	if (pattern.search(str(sentence))):
            print(str(sent_num) + ":\t" + str(sentence) + "\n")
            sent_num += 1