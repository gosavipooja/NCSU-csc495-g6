## Required Software
Either use base python or install Anaconda. Anaconda works really well for machine learning.

`sudo apt-get install python3`    
`pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose`  
`pip install -U scikit-learn`  
`pip install -U nltk`  
Run python  
>>> import nltk  
>>> nltk.download()  
NLTK Downloader all  

## Getting Dataset From LexisNexis Academic DB
1. Goto [LexisNexis Academic DB](http://www.lexisnexis.com/hottopics/lnacademic/?shr=t&sfi=AC00NBEasySrch)
2. Search for something like "Hospital and ___" 
3. Click the save button and save it as "TEXT" and set the "Selection" to "1-499"
4. Save the compiled text file

## How to split the huge text file into separate files
1. In Bash run `csplit FILENAME /DOCUMENT/ {*}`
