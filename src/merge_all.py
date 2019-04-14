import geopandas as gpd
import random
from shapely.geometry import Point
import math
import pandas as pd
import glob
import csv
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
from afinn import Afinn

# import US states shape file get california geo coordinate outline
state_boundary_us = gpd.read_file("./spacial-data/usa/usa-states-census-2014.shp")
state_boundary = state_boundary_us[['NAME', 'geometry']]
states_agg = state_boundary.dissolve(by='NAME', aggfunc='sum')
cali = states_agg[3:4]
cali.reset_index(level=0, inplace=True)
cal = cali.envelope  # california outline


# generates random coordinates and writes to napa_coordinates.txt
def generate_random(num, polygon):
    """This function take in a number of points to be generated and a polygon outline of the state in which you wish
    to generate data. The polygon for the state of california was generated above."""
    list_of_points = []
    vals = polygon.bounds
    minx = int(vals['minx'].values)
    miny = int(vals['miny'].values)
    maxx = int(vals['maxx'].values)
    maxy = int(vals['maxy'].values)
    counter = 0
    num_one = round(num * .5)  # .5 for the state
    num_two = round(num * .5)  # .5 for the concentrated radius

    for i in range(num_one):
        while counter < num_one:
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))

            if cali['geometry'].loc[0].contains(pnt):
                list_of_points.append(pnt)
                counter += 1

    geopoint = sum(map(list, (p.coords for p in list_of_points)), [])

    # randomly generated points around a focused radius
    radius = 160934  # Choose radius
    radius_in_degrees = radius / 111300
    r = radius_in_degrees
    x0 = 38.557428
    y0 = -121.501336

    for i in range(num_two):
        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))

        w = r * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)

        x_lat = x + x0
        xlong = y + y0
        geopoint.append(tuple((xlong, x_lat)))
    geopoint = random.sample(geopoint, len(geopoint))
    with open('napa_coordinates.txt', 'w') as fp:
        fp.write('\n'.join('{}, {}'.format(str(x[1]), str(x[0])) for x in geopoint))

# # # # # # # # # # # # # # # # # # #  # #  # # #  # #
# # # # # # # # Merge Predictions # # # # # # # # # #
# # # # # # # # # # # # # # # # # # #  # #  # # #  # #


# Merges predictions from AWS, sentiment scores, and geo coordinates into file for visualization
# path to unlabeled formatted tweet splits
path1 = "./unlabeled_california_from_website/formatted_tweets/tweets_california_formatted"
all_files = glob.glob(path1 + "*.txt")

# reads through all files and merges
li = []
for filename in all_files:
    df = pd.read_csv(filename, sep="\t", quoting=csv.QUOTE_NONE)
    li.append(df)
unlabeled = pd.concat(li, axis=0, ignore_index=True)
unlabeled = unlabeled.drop(['category'], axis=1)

# path to predictions.tsv
path2 = "./comprehend/predictions.tsv"
labels = pd.read_csv(path2, sep='\t')
df = pd.concat([unlabeled, labels], axis=1)
df['name'] = 'California'

print("Generating Coordinates...")
test = generate_random(len(df)-1, cal)
print("Coordinates Generated")

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
coords = pd.read_csv("napa_coordinates.txt", sep=",", header=None, names=["lat", "long"])
minimum = min([len(df),len(coords)])
coords = coords.head(minimum)
df = df.head(minimum)

df['lat'] = coords['lat'].values
df['long'] = coords['long'].values

df.to_csv('./california_labeled_formatted_tweets.txt', sep='\t')

# sanity check
print(df.head())
