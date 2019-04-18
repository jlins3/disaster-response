import math
import pandas as pd
import glob
import csv
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
from afinn import Afinn
import sys

# Merges predictions from AWS, sentiment scores, and geo coordinates into file for visualization
# path to unlabeled formatted tweet splits


def merge(nolabel, label):
    path1 = nolabel
    all_files = glob.glob(path1 + "*.txt")

    # reads through all files and merges
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, sep="\t", engine='python', quoting=csv.QUOTE_NONE)
        li.append(df)
    unlabeled = pd.concat(li, axis=0, ignore_index=True)
    unlabeled = unlabeled.drop(['category'], axis=1)

    # path to predictions.tsv
    path2 = label
    labels = pd.read_csv(path2, sep='\t')
    df = pd.concat([unlabeled, labels], axis=1)
    df['name'] = 'California'


    # clean tweets
    tweetsList = df['tweet'].tolist()
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        result = re.sub(r"http\S+", "", normalized)
        return result
    tweetsList_clean = [clean(tweet).split() for tweet in tweetsList]

    # run sentiment analysis on tweets
    afinn = Afinn()
    sentiments = [afinn.score(' '.join(tweet)) for tweet in tweetsList_clean]
    df['sentiment'] = sentiments

    # Reading in coordinates
    # coords = pd.read_csv("napa_coordinates.txt", sep=",", header=None, names=["lat", "long"])
    # minimum = min([len(df),len(coords)])
    # coords = coords.head(minimum)
    # df = df.head(minimum)
    #
    # df['lat'] = coords['lat'].values
    # df['long'] = coords['long'].values

    df.to_csv('./california_labeled_formatted_tweets.txt', sep='\t', header=True,index=False)

# # sanity check
# print(df.head())


if __name__ == '__main__':
    # get tweets for username passed at command line
    if len(sys.argv) == 3:
        merge(sys.argv[1], sys.argv[2])
    else:
        print("Error - Command line args missing")