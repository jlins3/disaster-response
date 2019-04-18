import csv
import json
import sys
import os

import pandas as pd
import tweepy

def read_tweetIDs(file_name):
    tweets = pd.read_csv(file_name)
    return tweets


# if we're running this as a script
if __name__ == '__main__':
    # get tweets for username passed at command line
    if len(sys.argv) == 3:
        for filename in os.listdir(sys.argv[2]):
            print(sys.argv[2]+filename)
            tweets = read_tweetIDs(sys.argv[2]+filename)
            tweets.to_csv(sys.argv[1],index=False,header=None,columns=["choose_one_category", "tweet_text"])
    else:
        print("Error")