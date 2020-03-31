import json
import re
import requests
import difflib
import pandas as pd
import urllib3
from pathlib import Path
import os



# requires, chunk of narrowed text and the word to search for
# returns the data points related to that word in a dictionary with
# the probability of it being a match
def search_text(word, text):
    matches = {}
    return matches


# requires, text of PDF and keywords to search for
# returns, chunks of text related to keywords to be searched
def extract(keywords, text):
    return_data = {}
    for word in keywords:
       return_data[word] = search_text(word, text)
    return return_data


# requires database link and list of keywords to filter searches by
# returns the text mined PDF of paper (will look into more exact data extraction)
def search_daily(link, keywords):
    return_data = {}
    r = requests.get(link)
    with open("today.xlsx", 'wb') as f:
        f.write(r.content)
    path = Path(Path.cwd() / 'today.xlsx')
    df= pd.read_excel(path)
    for index, row in df.iterrows():
       title_words = row['Title'].split()
       print(title_words)
       clause = False
       if clause:
            return_data[row['Title']] = extract(keywords, requests.get(link))
       break
    return
    return return_data


link = 'https://www.cdc.gov/library/docs/covid19/ONLY_newarticles_30March2020_Excel.xlsx'
keyphrases = ['Transmission rate', 'Total population', 'Latency period',
              'Reporting rate', 'Infectious period reported', 'Infectious period unreported',
              'Percent recovered', 'recover time', 'hospitalization rate', 'unreported hospitalization',
              'Percentage of hospitalized who needs ICU', 'Time from hospitalization to ICU', 'Percentage of ICU patients who recover',
              'Time from ICU admission to recovery', 'Percentage of ICU patients who die', 'Time from ICU admission to death']
search_daily(link, keyphrases)
