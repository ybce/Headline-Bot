from config import STOP, url, params
import requests
import requests
from thesaurus import Word


def new_headline(headline):
    head_list = headline.split()
    new_head = []
    for word in head_list:
        if word in STOP:
            new_head.append(word.upper())
            continue
        w = Word(word)
        syn = w.synonyms()
        if syn:
            new = syn[0]
            new_head.append(new.upper())
        else:
            new_head.append(word.upper())
    new_headline_string=(' ').join(new_head)
    return new_headline_string



def get_nyt_headlines_with_url():

    r = requests.get(url, params=params)
    docs = r.json()['response']['docs']
    headlines = []
    for i in range(0, len(docs)):
        headlines.append((docs[i]['headline']['main'], docs[i]['web_url']))

    return headlines[0]