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


# requires list of links of databases to check
# returns the text mined PDF of paper (will look into more exact data extraction)
def search_daily(link, keywords):
    return_data = {}
    r = requests.get(link)
    with open("data.xlsx", 'wb') as f:
        f.write(r.content)
    path = Path(Path.cwd() / 'data.xlsx')
    df= pd.read_excel(path)
    print(df.columns)
    return
    for index, row in df.iterrows():
       title = row['Title']

    return_data[link] = extract(keywords, requests.get(link))
    return return_data


link = 'https://www.cdc.gov/library/docs/covid19/ONLY_newarticles_30March2020_Excel.xlsx'
keywords = ['corona']
search_daily(link, keywords)

# print(search_daily(links, keywords))
