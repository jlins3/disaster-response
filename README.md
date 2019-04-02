# disaster-response

Using twitter data to make predictions and visualizations about natural disasters

## Overview

In the digital age, news about crisis and major events gets reported fastest on social media sites like Twitter, even before traditional news channels can report. We think there is a need for an analytics solution that can tap into this information and provide valuable insights to social aid workers, first responders, government, and people in need to help them better respond to these events and potentially save lives. 

We will focus on processing Twitter feeds (tweets) with hashtags associated with disasters and group them into categories like health, food and safety, and build visualizations on these insights to help organizations more quickly scan the geography for the different categories of problems and respond in a timely manner, through effective resource allocation. 

We will apply topic analysis and sentiment analysis to tweets related to specific disasters using Python, AWS cloud technology and D3 for interactive visualization. 

## Process/Methods
The building portion of this project consists of four phases:
1.	Data gathering
2.	Model Building 
3.	Visualization 
4.	Real Time Simulation
These phases have been carried out concurrently. 

1.	Data Gathering 

The first step is this project, after determining the data source, is gathering the data. The website “CrisisNLP” has several crises related twitter datasets, with human labeled tweets for training a machine learning model. The labels describe the category of the tweet, such as caution and advice, not related or irrelevant, displaced people and evacuations, infostructure and utilities damage, etc. We can download these data for the California earthquake at the bottom of the page.

2.	Model Building
The next step in this process is to begin building a model. There are several sub steps here such as data cleaning, exploration, feature selection, etc. which are discussed in further detail in the available notebooks. The file california_classification.py can be used to build the model and then, predict the category of the unlabeled tweets. 

3.	Visualization
This step happens during the model building phase and after. Most of the visualization for this project was done with D3.js, while some exploratory visualization was done in python. 



## How to Install
To download, just do this:

## How to Run
To run the project, simply follow these steps:
1.
2.
3.



References:
D3.js book
Python NLP book
https://crisisnlp.qcri.org/lrec2016/lrec2016.html (crisis NLP)
https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f
