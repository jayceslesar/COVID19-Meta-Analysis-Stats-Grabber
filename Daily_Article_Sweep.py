import json
import re
import ast
import requests
from difflib import SequenceMatcher
import pandas as pd
import urllib3
from pathlib import Path
from datetime import date
import datetime
import lxml.html


def parse_articles(article, words):
    stats = {}
    return stats


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_relevant_titles(title, keywords, bad_keywords):
    title_words = [word.lower() for word in title.split(' ')]
    for bad in bad_keywords:
        if bad.lower() in title_words:
            return False
    probs = []
    for keyword in keywords:
        for title_word in title_words:
            if len(title_word) > 2:
                if similar(title_word, keyword.lower()) > 0.75:
                    probs.append(True)
    if len(probs) > 1:
        return True
    else:
        return False


class Daily_Article_Sweep:
    # initializer
    def __init__(self):
        today = date.today()
        d2 = today.strftime("%B %d %Y").split()
        if d2[1][0] == '0':
            day = d2[1][1:]
        self.DATE = day + d2[0] + d2[2]
        yesterday = date.today() - datetime.timedelta(days=1)
        d2 = yesterday.strftime("%B %d %Y").split()
        if d2[1][0] == '0':
            day = d2[1][1:]
        self.DATE_YESTERDAY = day + d2[0] + d2[2]
        self.CDC_LINK = 'https://www.cdc.gov/library/researchguides/2019novelcoronavirus/researcharticles.html'
        self.CDC_PAPERS = 'https://www.cdc.gov'
        self.JSON_PAPERS = 'https://connect.medrxiv.org/relate/collection_json.php?grp=181'
        self.KEYPHRASES = ['transmission', 'rate', 'population', 'Latency', 'period', 'spread',
                           'Reporting', 'rate', 'Infectious', 'reported', 'unreported', 'hospital',
                           'Percent', 'recovered', 'recover' , 'time', 'hospitalization', 'Percentage', 'hospitalized', 'ICU',
                           'from', 'patients', 'admission', 'die', 'death', 'differential', 'equations', 'susceptible',
                           'exposed', 'model', 'modelling', 'infected', 'risk', 'infection', 'infect']
        self.BAD_KEYWORDS = ['gene', 'ACE2',
                             'chloroquine', 'remdesivir', 'favipiravir', 'rhinitis']
        self.todays_matches = []
        self.DROPPED = 0

        def get_cdc(self):
            matches = []
            page = requests.get(self.CDC_LINK).text
            tree = lxml.html.fromstring(page)
            link = tree.xpath(
                '/html/body/div[6]/main/div[3]/div/div[3]/div[2]/div[2]/div/div[2]/ul[1]/li[2]/a')[0]
            rest = link.attrib['href']
            r = requests.get(self.CDC_PAPERS + rest)
            with open("today.xlsx", 'wb') as f:
                f.write(r.content)
            path = Path(Path.cwd() / 'today.xlsx')
            df = pd.read_excel(path)
            for index, row in df.iterrows():
                curr_match = {}
                curr_title = row['Title']
                if 'withdrawn' in curr_title.lower():
                    continue
                if curr_title[0] == '[':
                    curr_title = curr_title[1:-1]
                if find_relevant_titles(curr_title, self.KEYPHRASES, self.BAD_KEYWORDS):
                    curr_match["title"] = curr_title
                    if type(row['URL']) != float and 'ovid' in row['URL']:
                        curr_match["link"] = row['DOI']
                    else:
                        curr_match["link"] = row['URL']
                    self.todays_matches.append(curr_match)
                else:
                    self.DROPPED += 1

        def get_rxiv(self):
            data = requests.get(self.JSON_PAPERS).json()
            matches = []
            for paper_data in data["rels"]:
                curr_title = paper_data["rel_title"]
                curr_match = {}
                if find_relevant_titles(curr_title, self.KEYPHRASES, self.BAD_KEYWORDS):
                    curr_match["title"] = curr_title
                    curr_match["link"] = paper_data["rel_link"]
                    self.todays_matches.append(curr_match)
                else:
                    self.DROPPED += 1

        get_cdc(self)
        get_rxiv(self)
        self.todays_data_df = pd.DataFrame(self.todays_matches)
        self.todays_data_df.to_csv('daily_to_search.csv')
        print('Filters cleared out ' + str(self.DROPPED) + ' irrelevant articles.')
        print('Found ' + str(len(self.todays_matches)) + ' potential matches.')
