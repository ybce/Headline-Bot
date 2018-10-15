from TwitterAPI import TwitterAPI
from config import TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_ACCESS_TOKEN_KEY, TW_ACCESS_TOKEN_SECRET
from utils import get_nyt_headlines_with_url, new_headline

def tweet(event, context):
    api = TwitterAPI(TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_ACCESS_TOKEN_KEY, TW_ACCESS_TOKEN_SECRET)
    headline = get_nyt_headlines_with_url()

    headline_text = headline[0]
    headline_url = headline[1]

    headline = new_headline(headline_text)

    status = headline+' '+headline_url

    new_tweet = {"status": status}

    r = api.request("statuses/update", params=new_tweet)

    return r.json()

