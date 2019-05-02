# -*- coding: utf-8 -*-
import tweepy

consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

public_tweets = api.home_timeline()

with open("tweets.txt","a") as f:
    for tweet in public_tweets:
        d = str(unicode(tweet.text).encode('utf-8'))
        f.writelines(d)
    f.close()
