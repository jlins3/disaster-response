# Description

We believed that there is a need for an analytics solution that can tap into the vast information that twitter brings and
provide valuable insights to social aid workers, first responders, government, and people in need to help them better respond
to crisis events and potentially save lives. This package focuses on processing Twitter feeds (tweets) with hashtags associated
with disasters and grouping them into categories like infrastructure, injured people, and caution and advice, and build visualizations
of these insights to help organizations more quickly scan the geography for the different categories of problems and respond in a
timely manner, through effective resource allocation.

This package contains a python script to download tweets and instructions to format tweets to be used in AWS set up a classifier to generate predictions of classifications of tweets using AWS comprehend.
We then take the output from comprehend and reformat that data to be usable in our visualization. We also provide in a script the tools necessary to
generate random coordinates and ensure that coordinates used in the visualization are within the bounds of the area of interest.
This file also contains the code needed to generate sentiment scores for each of the tweets. Finally, we use D3.js to generate an interactive visualization
that allows the user to explore the dataset and filter for attributes like time, and the category label, and visually pinpoint the location of the tweet,
exact time and date, the sentiment value, and the tweet itself.

Below are the instructions to run a demo given a subset of the data and then further instructions on how to recreate this project yourself.

===============================================================================

# Installation

### Step 0. Set up Twitter developer account at the following link: https://developer.twitter.com/en/docs/basics/getting-started

Create Twitter application and develop the credentials required to run the script. These
are: consumer_key, consumer_secret, access_key, and access_secret. These will be needed
to download tweets in the file tweet_downloader.py discussed below.

The folder structure for this project will be as shown below. Refer to this throughout.
The Data folder will contain all data we use in this project and CODE will contain the
python scripts needed.

CODE
  -Data
      -comprehend
      -CrisisNLP_labeled_data_crowdflower
      -formatted_tweets
          -unlabeled
          -labeled
      -Geo
      -spacial-data
          -usa
              -shape files
      -tweet_ids
          -labeled
          -unlabeled
      -tweets
          -labeled
          -unlabeled
  -Scripts
      -merge_all.py
      -tweet_formatter.py
      -geo.py
      -getPredictions.py
      -get_labeled_tweets.py
      -tweet_downloader.py

  -visualize
  -lib


For now create the following structure and ensure that the python files are saved:

CODE
    -Data
      -tweet_ids
      -labeled


    -merge_all.py
    -tweet_formatter.py
    -geo.py
    -getPredictions.py
    -get_labeled_tweets.py
    -tweet_downloader.py

### Step 1. Download labeled data from the Crisis NLP website

https://crisisnlp.qcri.org/lrec2016/lrec2016.html
This link contains labeled and unlabeled tweets from several natural disasters.

Ensure you have the folder structure CODE\Data\tweet_ids\labeled. This is where we will save the labeled data.

To download the labeled tweets, go to the bottom of the Crisis NLP page and click on the first option: Labeled data annotated by paid workers for all the events.
In this zip file, navigate to the 2014_California_Earthquake folder and save 2014_california_eq.csv to CODE\data\tweet_ids\labeled.
You should now have CODE\data\tweet_ids\labeled\2014_california_eq.csv

### Step 2. Extract the category and tweet columns to create the training data set for the classifier.

Create the folder structure CODE\data\formatted_tweets\labeled. The script get_labeled_tweets.py generates a formatted training dataset for AWS Comprehend.
In the command line type python get_labeled_tweets.py Data\formatted_tweets\tweets.txt Data\tweet_ids\labeled\

This will create a file tweets.txt in the folder Data\formatted_tweets\labeled\tweets.txt which will be used in AWS comprehend.

### Step 3. AWS comprehend

For more detailed instructions with screenshots, open the AWS Comprehend document in the recourses folder.

a.	Open the console.aws,amazon.com website, login with your credentials and click on S3 from the list of services under the Storage category.
b.	Click create bucket, give it a name and click next on all options, then “create bucket”. We will use this bucket to upload our training data. Name this folder californiatweets.
c.  Create two subfolders labeled and unlabeled
c.	Upload tweets.txt to the labeled folder
d.	Click on AWS Comprehend from the list of services under the Machine Learning category.
e.	This will bring up the landing page of AWS Comprehend, with an orange button Launch Comprehend. Click on it to bring up the AWS Comprehend console.
f.	Click on the Custom Classification menu item on the right and then click the orange “Train Classifier” button to create a new classifier.
g.	Give it a name, and the location of the file in S3 where we have uploaded the training data, californiatweets\labaled\tweets.txt The training data needs to have two fields and be in .txt format.
For ex:  CAT1, Text1 where CAT1 is the category of classification (class variable) and Text1 is the tweet in our case.
h.	Select the create an IAM role option and leave the default selection
i.	Under name suffix, give a name of your choosing
j.	Click on the Train Classifier button.

After few minutes, the classifier will be trained, and the performance metrics will be displayed. In our case, the accuracy was 0.6766, precision: 0.5302, recall: 0.498 and F1 score: 0.50.
The overall accuracy is better than random coin flip, but further text preprocessing could have been done to bring up the overall precision and recall scores.

### Step 4. Generate coordinates

Ensure you have the file structure CODE\Data\Geo

To generate coordinates, in the command line, from the Scripts folder run >python geo.py [# of coordinates]
Here the number of coordinates will depend on the dataset you are using. Our dataset consists of 126076 unlabeled tweets, thus
the command will be >python geo.py 126075 Data\Geo

This generates napa_coordinates.txt. Move this to the CODE\Data\Geo folder.

### Step 5. Download Unlabeled dataset

Ensure you have the folder structure CODE\Data\tweet_ids\unlabeled

https://crisisnlp.qcri.org/lrec2016/lrec2016.html
This link contains labeled tweets to build a classifier and unlabeled tweets from several natural disasters.
To download the unlabeled tweets, click on the California link and download the fulltweetsIds.zip folder which
contains files of tweetid, userid tuples. This will be used to generate the unlabeled tweets dataset.

In the folder CODE\Data\ , unzip the downloaded tweets. In this zip file are 4 CSV files with tweet id and user id information.
Move these to the CODE\Data\tweet_ids\unlabeled folder.

If you do not already have tweepy installed you can install by running easy_install tweepy in the command line [Windows].

Open the command line and navigate to the DTV directory. Run the command
'>py tweet_downloader.py Data\tweets\unlabeled\tweets.txt Data\tweet_ids\unlabeled\' [Windows]

This can take roughly 30 minutes depending upon your internet speed.


### Step 6. Format and split the unlabeled dataset by running tweet_formatter.py

Ensure you have the file structure CODE\Data\formatted_tweets\unlabeled

In the command line navigate to the Scripts directory and run the following:

>python tweet_formatter.py Data\tweets\unlabeled\tweets.txt Data\formatted_tweets\unlabeled\tweets Data\Geo\napa_coordinates.txt

It will generate two files,
1: tweets_split.txt with all the data needed for visualization [categories]
2: tweets_all.txt with just the tweet text. We will use AWS comprehend to classify these tweets into one of the disaster categories.

This process can take 15 or more minutes depending on your computers speed.

Create a folder named tweets_all in CODE\Data\formatted_tweets\unlabeled and move tweets_all.txt and tweets_classes_all.txt to this folder.

### 7. Predict the categories of the unclassified tweets in AWS comprehend.

a.	Upload unlabeled data to S3 in the californiatweets\unlabeled folder. Create a the path californiatweets\unlabeled\output.
b.	Click on the trained classifier and click on the “Create job” button.
c.	Give the job a name, and ensure the Analysis type is set to Custom Classification and Select Classifier is pointing to the classifier trained above.
d.	For input data provide a location of the file in S3, where the data to be classified is uploaded (unlabeled). The input data should have one field which is the tweet that needs to be classified.
e.	Provide the S3 location where we want the output of the job to be placed, californiatweets\unlabeled\output. This is the file tweets_classes_all.txt in the formatted_tweets\unlabeled\tweets_all folder
f.	Select the Create a new IAM role option
g.	Click on the “Create Job” button.


### 8. Parse the predictions.json file to extract out only the categories

Once the comprehend job is complete, go to AWS and navigate to the s3\californiatweets\unlabeled\output\(jobid)\output.
Download the output.gz file. Create a new folder on your desktop\CODE\data\comprehend. Unzip the contents here.
In this folder will be predictions.jsonl file. To turn this data into a format that can be merged with the unlabeled data,
run the following command in the command line: >python getPredictions.py Data\comprehend\predictions.jsonl Data\comprehend\predictions.tsv
This generates a predicted category corresponding to each of the unlabeled tweets.

### 9. Create a new file with all the fields from (filename) and add the geocoordinates and category information predicted in step 7 and perform sentiment analysis.

The script merge.py does the sentiment analysis on the tweets and adds the sentiment scores as an additional column to the data set along with the category that was predicted by AWS Comprehend in step 7.

Ensure that in CODE\Data\formatted_tweets\unlabeled there are a series of tweets0 - tweeets50 text files and a folder tweets_all that contains tweets_all.txt and tweets_classe s_all.txt

In the command line, in the Scripts folder, execute the following: >python merge_all.py Data\formatted_tweets\unlabeled\tweets Data\comprehend\predictions.tsv

This will create a california_labeled_formatted_tweets.txt in the same folder as the script.

### 10. Visualization

Move the california_labeled_formatted_tweets.txt file to the visualize folder and change the path in index.html to read this file in and follow exactly the steps below.

===============================================================================

# Execution

DEMO:
Here we give a brief set of instructions to set up and run the project.

Note: Chrome is the only browser tested and therefore known to work with this project

1. Unzip the contents of team39final.zip
2. Open a terminal window, cd to the CODE folder (contains lib and visualize folders), and execute 'http-server' to serve up the project files
3. In your browser go to http://localhost:8080/visualize

To interact with the visualization, do the following:

a. On the time slider at the bottom, change the range to whatever time range you want to view. If you keep it at the default of zero you will see no points.
b. You can move the time slider back and forth to see how the data changes over time.
c. You can click the play/pause button to the left of the time slider to automatically step through the data chronologically.
d. The legend is interactive and allows you to show/hide the topics of interest by simply clicking on the color.
e. Upon hovering over a node, a tooltip with pertinent data about the node will appear and disappear when the cursor moves off of the node.
f. You can zoom and pan the map using your mouse (scroll wheel to zoom and left-button-down+drag to pan)
