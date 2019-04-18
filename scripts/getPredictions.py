#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import sys
import os

import pandas as pd
import tweepy

def process_predictions(input, output): # predictions.json, predictions.tsv
    with open(input, "r") as input_file:
        line = input_file.readline()
        cnt = 1
        while line:
            json_text = json.loads(line)
            #print(json_text["Classes"][0]["Name"])
            with open(output, "a+") as output_filename:
                if (cnt==1):
                    output_filename.write ("category\n")
                output_filename.write(json_text["Classes"][0]["Name"]+"\n")
            line = input_file.readline()
            cnt = cnt + 1

# if we're running this as a script
if __name__ == '__main__':
    # get tweets for username passed at command line
    if len(sys.argv) == 3:
        process_predictions(sys.argv[1], sys.argv[2])
    else:
        print("Error")