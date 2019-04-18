#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import sys
import os

import pandas as pd
import tweepy

# Get your Twitter API credentials and enter them here
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def read_tweetIDs(file_name):
    tweets = pd.read_csv(file_name)
    return tweets

def write_tweets_to_file(tweets, filename):
     with open(filename, "a+") as output:
            [output.write(json.dumps(x._json)+"\n") for x in tweets]

def lookup_tweets(tweet_IDs, filename):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                        wait_on_rate_limit_notify=True)
    full_tweets = []
    tweet_count = len(tweet_IDs)
    tweets_by_100 = int(tweet_count/100)
    remaining_tweets = int(tweet_count%100)
    print(tweet_count,tweets_by_100,remaining_tweets)
    for i in range(0,tweets_by_100):
       print(i)
       try:
           tweets = api.statuses_lookup(tweet_IDs[i*100:(i+1)*100])
           write_tweets_to_file(tweets,filename)

       except tweepy.TweepError as e:
           print(e)
    try:
            tweets = api.statuses_lookup(tweet_IDs[tweets_by_100*100:tweets_by_100*100+remaining_tweets])
            write_tweets_to_file(tweets,filename)

    except tweepy.TweepError as e:
           print(e)

    return full_tweets
	


# if we're running this as a script
if __name__ == '__main__':
    # get tweets for username passed at command line
    if len(sys.argv) == 3:
        for filename in os.listdir(sys.argv[2]):
            print(sys.argv[2]+filename)
            tweetIDs = read_tweetIDs(sys.argv[2]+filename)
            tweetIDs = tweetIDs.tweet_id.tolist()

            tweetIDs = [str(x).replace("'","") for x in tweetIDs]      
            print(len(tweetIDs))
            #print(tweetIDs)
            tweets = lookup_tweets(tweetIDs, sys.argv[1])
    else:
        print("Error")
