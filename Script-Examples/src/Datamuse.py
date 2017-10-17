'''
    Rest Api to datamuse which lets us easily get synonmys of words
'''


import requests

baseAPI = 'https://api.datamuse.com/words?'
meansLike = 'ml='

def getMeansLikeList(word):
    request = baseAPI + meansLike + word
    response = makeRequest(request)

    synonyms = []
    if response:
        synonyms.append(word)
        for wordObj in response:
            synonyms.append(wordObj['word'])

    return synonyms

def makeRequest(request):
    return requests.get(request).json()