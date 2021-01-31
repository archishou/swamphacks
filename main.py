from __future__ import print_function
import requests
import time
import json
import sys
import twitter
from twilio.rest import Client

client = Client("ACc52c75209500e9dbc4f046fc3979a8c7", "8f4281143bfcf6cbc3b4e8ceeb7d1f80")
consumer_key ="PbOsBxtz6yYvv4aNqI1RZpF2L"
consumer_key_sec = "6Fog2uWthJ2c20XeP8Yr3EPDwwoMmpTTirCs0P1NfRswkb9tC7"
token = "3328669373-KtVD68tH5pImIZqwa5mCLMFyOr35W1tr2BpxXkd"
token_sec = "xwPJSUJTnZ3cDUT2rLZgo7AuPk1Kf3Vbf4mWFmuR4Iotk"
bearer = "AAAAAAAAAAAAAAAAAAAAAIwaMQEAAAAAnEGbs0ZcJCYzS0nCuyt7VZcConk%3Da7d5qMQOysM2TNf5Kh7SutVA7F4K2nF0ZoFPVQWxhqecIQuMQD" 

def get_symbol(symbol):
    symbol = symbol.replace("$", "")
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']

def tweet_contains_sym(tweet):
    words = tweet.split()
    for word in words:
        print(word)
    for word in words:
        if str(get_symbol(word)) != "None":
            return get_symbol(word)

    return "None"

def send_text(mssg):
    client.messages.create(to="+18137345578", 
                       from_="+17196940306", 
                       body=mssg)

def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


if __name__ == "__main__":
    api = twitter.Api(
        consumer_key, consumer_key_sec, token, token_sec
    )
    screen_name = sys.argv[1]
    print(screen_name)
    print(str(get_symbol("$TSLA"))) 
    i = 0
    timeline = get_tweets(api=api, screen_name=screen_name)
    old_tweet_count = len(timeline) 
    while i < 120:
        print("refreshing")
        timeline = get_tweets(api=api, screen_name=screen_name)
        if old_tweet_count != len(timeline):
            latest_tweet = timeline[0]._json['text']
            symb = str(tweet_contains_sym(latest_tweet))
            if symb != "None":
                send_text(screen_name + " tweeted about " + symb)
            else:
                print("new tweets but no stocks")
        old_tweet_count = len(timeline)
        time.sleep(1)
        i = i + 1
