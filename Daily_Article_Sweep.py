import json
import re
import ast
import requests
import difflib
import pandas as pd
import urllib3
from pathlib import Path
from datetime import date



class Daily_Article_Sweep:

    def __init__(self):
        today = date.today()
        d2 = today.strftime("%B %d %Y").split()
        self.DATE = d2[1] + d2[0] + d2[2]
        self.EXCEL_PAPERS = 'https://www.cdc.gov/library/docs/covid19/ONLY_newarticles_' + self.DATE + '_Excel.xlsx'
        self.JSON_PAPERS = 'https://connect.medrxiv.org/relate/collection_json.php?grp=181'
        self.KEYPHRASES = ['Transmission rate', 'Total population', 'Latency period',
                        'Reporting rate', 'Infectious period reported', 'Infectious period unreported',
                        'Percent recovered', 'recover time', 'hospitalization rate', 'unreported hospitalization',
                        'Percentage of hospitalized who needs ICU', 'Time from hospitalization to ICU', 'Percentage of ICU patients who recover',
                        'Time from ICU admission to recovery', 'Percentage of ICU patients who die', 'Time from ICU admission to death']


    def get_excel(self):
        return_data = {}
        r = requests.get(self.EXCEL_PAPERS)
        with open("today.xlsx", 'wb') as f:
            f.write(r.content)
        path = Path(Path.cwd() / 'today.xlsx')
        df = pd.read_excel(path)
        for index, row in df.iterrows():
            curr_title = row['Title']
            if curr_title[0] == '[':
                curr_title = curr_title[1:-1]
            title_words = curr_title.split(' ')
            print(title_words)
            # clause = False
            # if clause:
            #     return_data[row['Title']] = extract(keywords, requests.get(link))
            break
        return
        return return_data

    #def get_json(self):
