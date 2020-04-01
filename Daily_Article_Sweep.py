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


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_relevant_titles(title, keywords):
    title_words = [word.lower() for word in title.split(' ')]
    if 'gene' in title_words:
        return False
    probs = []
    for keyword in keywords:
        for title_word in title_words:
            if len(title_word) > 2:
                if similar(title_word, keyword.lower()) > 0.65:
                    probs.append(True)
    if len(probs) > 1:
        return True
    else:
        return False

class Daily_Article_Sweep:

    def __init__(self):
        today = date.today()
        d2 = today.strftime("%B %d %Y").split()
        self.DATE = d2[1] + d2[0] + d2[2]
        yesterday = date.today() - datetime.timedelta(days=1)
        d2 = yesterday.strftime("%B %d %Y").split()
        self.DATE_YESTERDAY = d2[1] + d2[0] + d2[2]
        self.EXCEL_PAPERS = 'https://www.cdc.gov/library/docs/covid19/ONLY_newarticles_' + self.DATE + '_Excel.xlsx'
        self.EXCEL_PAPERS_YESTERDAY = 'https://www.cdc.gov/library/docs/covid19/ONLY_newarticles_' + \
            self.DATE_YESTERDAY + '_Excel.xlsx'
        self.JSON_PAPERS = 'https://connect.medrxiv.org/relate/collection_json.php?grp=181'
        self.KEYPHRASES = ['Transmission', 'rate', 'population', 'Latency', 'period',
                           'Reporting', 'rate', 'Infectious', 'reported', 'unreported', 'hospital',
                           'Percent', 'recovered', 'recover' , 'time', 'hospitalization', 'Percentage', 'hospitalized', 'ICU',
                           'from','patients', 'admission', 'die', 'death']
        self.todays_matches = []

        def get_excel(self):
            matches = []
            r = requests.get(self.EXCEL_PAPERS)
            with open("today.xlsx", 'wb') as f:
                f.write(r.content)
            path = Path(Path.cwd() / 'today.xlsx')
            try:
                df = pd.read_excel(path)
            except:
                r = requests.get(self.EXCEL_PAPERS_YESTERDAY)
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
                if find_relevant_titles(curr_title, self.KEYPHRASES):
                    curr_match["title"] = curr_title
                    if type(row['URL']) != float and 'ovid' in row['URL']:
                        curr_match["link"] = row['DOI']
                    else:
                        curr_match["link"] = row['URL']
                    self.todays_matches.append(curr_match)

        def get_json(self):
            data = requests.get(self.JSON_PAPERS).json()
            matches = []
            for paper_data in data["rels"]:
                curr_title = paper_data["rel_title"]
                curr_match = {}
                if find_relevant_titles(curr_title, self.KEYPHRASES):
                    curr_match["title"] = curr_title
                    curr_match["link"] = paper_data["rel_link"]
                    self.todays_matches.append(curr_match)

        get_excel(self)
        get_json(self)
        self.todays_data_df = pd.DataFrame(self.todays_matches)
        self.todays_data_df.to_csv('search_these_links.csv')



