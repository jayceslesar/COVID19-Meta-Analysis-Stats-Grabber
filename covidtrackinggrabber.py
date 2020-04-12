import requests
import pandas as pd
from pathlib import Path
import json

cwd = Path.cwd()
def get_data():
    link = 'https://covidtracking.com/api/v1/states/daily.json'
    all_data = {}
    states = []
    data = requests.get(link).json()
    for date in data:
        states.append(date["state"])
    states = list(set(states))
    for state in states:
        all_data[state] = []
    for date in data:
        date.pop('hash')
        date.pop('dateChecked')
        for state in states:
            if date["state"] == state:
                all_data[state].append(date)
    for state in all_data.keys():
        curr_state = reversed(all_data[state])
        df = pd.DataFrame(curr_state)
        path = Path(cwd / 'data')
        df.to_csv(str(path) + '/' + state + '.csv')
    us = 'https://covidtracking.com/api/us/daily'
    us_data = requests.get(us).json()
    us_reversed = reversed(us_data)
    df = pd.DataFrame(us_reversed)
    path = Path(cwd / 'data')
    df.to_csv(str(path) + '/all_us.csv')


def main():
    get_data()


if __name__ == "__main__":
    main()

