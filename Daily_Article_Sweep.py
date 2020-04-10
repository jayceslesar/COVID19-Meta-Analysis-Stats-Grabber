import json
import re
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


# used to tell how similar to strings are
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# searches the title words and keywords list provided to ween out titles
# if it hits a good keyword it auto passes
# if it hits a bad keyword it auto failes
# otherwise it needs at least 2 other keywords to pass
def find_relevant_titles(title, keywords, bad_keywords, good_keywords):
    title_words = [word.lower() for word in title.split(' ')]
    for good in good_keywords:
        if good.lower() in title_words:
            return True
    for bad in bad_keywords:
        if bad.lower() in title_words:
            return False
    probs = []
    for keyword in keywords:
        for title_word in title_words:
            if len(title_word) > 2:
                # strings need to match at least 75% (forms of word accounted for here)
                if similar(title_word, keyword.lower()) > 0.75:
                    probs.append(True)
    if len(probs) > 2:
        return True
    else:
        return False


# class to organize data and run everything
class Daily_Article_Sweep:
    # initializer
    def __init__(self):
        # date formatting to get the right URL
        today = date.today()
        d2 = today.strftime("%B %d %Y").split()
        if d2[1][0] == '0':
            day = d2[1][1:]
        else:
            day = d2[1]
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
        self.GOOD_KEYWORDS = ['infection']
        self.todays_matches = []
        self.DROPPED = 0

        # parses the CDC database for relevant titles
        def get_cdc(self):
            # get the text data
            page = requests.get(self.CDC_LINK).text
            # lxml great to use for organzing html
            tree = lxml.html.fromstring(page)
            link = tree.xpath(
                '/html/body/div[6]/main/div[3]/div/div[3]/div[2]/div[2]/div/div[2]/ul[1]/li[2]/a')[0]
            # find the spreadsheet link
            rest = link.attrib['href']
            # download and open the spreadhsset
            r = requests.get(self.CDC_PAPERS + rest)
            with open("today.xlsx", 'wb') as f:
                f.write(r.content)
            path = Path(Path.cwd() / 'today.xlsx')
            # read into pandas
            df = pd.read_excel(path)
            # loop over every title
            for index, row in df.iterrows():
                curr_match = {}
                curr_title = row['Title']
                # withdrawn is a keyword CDC uses to say the article has been withdrawn
                if 'withdrawn' in curr_title.lower():
                    continue
                # string fixing in title
                if curr_title[0] == '[':
                    curr_title = curr_title[1:-1]
                # run the relevant function (function returns True or False)
                if find_relevant_titles(curr_title, self.KEYPHRASES, self.BAD_KEYWORDS, self.GOOD_KEYWORDS):
                    curr_match["title"] = curr_title
                    if type(row['URL']) != float and 'ovid' in row['URL']:
                        curr_match["link"] = row['DOI']
                    else:
                        curr_match["link"] = row['URL']
                    self.todays_matches.append(curr_match)
                else:
                    self.DROPPED += 1

        # parses the rxiv pre-release database
        def get_rxiv(self):
            # pings and gets the json object of daily info
            data = requests.get(self.JSON_PAPERS).json()
            # search each title
            for paper_data in data["rels"]:
                curr_title = paper_data["rel_title"]
                curr_match = {}
                # run the relevant function (function returns True or False)
                if find_relevant_titles(curr_title, self.KEYPHRASES, self.BAD_KEYWORDS, self.GOOD_KEYWORDS):
                    curr_match["title"] = curr_title
                    curr_match["link"] = paper_data["rel_link"]
                    self.todays_matches.append(curr_match)
                else:
                    self.DROPPED += 1
        # actualy run both functions
        get_cdc(self)
        get_rxiv(self)
        # create dataframe and save it
        self.todays_data_df = pd.DataFrame(self.todays_matches)
        self.todays_data_df.to_csv('daily_to_search.csv')
        print('Filters cleared out ' + str(self.DROPPED) + ' irrelevant articles.')
        print('Found ' + str(len(self.todays_matches)) + ' potential matches.')
