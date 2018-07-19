from TwitterAPI import TwitterAPI
import requests
from thesaurus import Word
import boto3
from config import json_content, STOP
import json


TW_CONSUMER_KEY = json_content['TW_CONSUMER_KEY']
TW_CONSUMER_SECRET = json_content['TW_CONSUMER_SECRET']
TW_ACCESS_TOKEN_KEY = json_content['TW_ACCESS_TOKEN_KEY']
TW_ACCESS_TOKEN_SECRET = json_content['TW_ACCESS_TOKEN_SECRET']
NYT_API_KEY = json_content['NYT_API_KEY']

url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

params = {
    "api-key": NYT_API_KEY,
    "sort": "newest",
}


def newHeadline(headline):
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


def getNYTHeadlinesWithUrl():

    r = requests.get(url, params=params)
    docs = r.json()['response']['docs']
    headlines = []
    for i in range(0, len(docs)):
        headlines.append((docs[i]['headline']['main'], docs[i]['web_url']))

    return headlines[0]


def tweet(event, context):
    api = TwitterAPI(TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_ACCESS_TOKEN_KEY, TW_ACCESS_TOKEN_SECRET)
    headline = getNYTHeadlinesWithUrl()

    headline_text = headline[0]
    headline_url = headline[1]

    new_headline = newHeadline(headline_text)

    status = new_headline+' '+headline_url

    new_tweet = {"status": status}

    r = api.request("statuses/update", params=new_tweet)

    return r.json()

