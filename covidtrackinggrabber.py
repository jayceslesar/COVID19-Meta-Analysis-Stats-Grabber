import requests
import pandas as pd
from pathlib import Path
import json



states_dict = {'CA': 39747267, 'TX': 29087070, 'FL': 21646155, 'NY': 19491339, 'PA': 12813969, 'IL': 12700381, 'OH': 11718568,
               'GA': 10627767, 'NC': 10497741, 'MI': 10020427, 'NJ': 8936547, 'VA': 8626107, 'WA': 7797095, 'AZ': 7378494,
               'MA': 6976597, 'TN': 6897576, 'IN': 6457354, 'MO': 6169270, 'MD': 6083116, 'WI': 5851754, 'CO': 5845516,
               'MN': 5700671, 'SC': 5210095, 'AL': 4908621, 'LA':4645184, 'KY': 4499692, 'OR': 4301089, 'OK': 3954821,
               'CT': 3563077, 'UT': 3282115, 'IA': 3179849, 'NV': 3139658, 'AR': 3038999, 'PR': 3032165, 'MS': 2989260,
               'KS': 2910357, 'NM': 2096640, 'NE': 1952570, 'ID': 1826156, 'WV': 1778070, 'HI': 1412687, 'NH': 1371246,
               'ME': 1345790, 'MT': 1086759, 'RI': 1056161, 'DE': 982895, 'SD': 903027, 'ND': 761723, 'AK': 734002,
               'DC': 720687, 'VT': 628061, 'WY': 567025}


master = pd.DataFrame()
to_master = []
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
        week = 1
        count = 0
        for day in curr_state:
            day_dict = {}
            if count == 7:
                week += 1
                count = 0
            if count == 0:
                day_dict['State'] = day['state']
                day_dict['Week after outbreak'] = week
                if 'positive' in day.keys():
                    day_dict['Confirmed cases'] = day['positive']
                else:
                    day_dict['Confirmed cases'] = 0
                if 'death' in day.keys():
                    day_dict['Deaths'] = day['death']
                else:
                    day_dict['Deaths'] = 0
                if 'hospitalizedCumulative' in day.keys():
                    print(day['hospitalized'])
                    day_dict['Hospitalized (cumulative)'] = day['hospitalizedCumulative']
                elif 'hostpitalized' in day.keys():
                    print(day['hospitalized'])
                    day_dict['Hospitalized (cumulative)'] = day['hospitalized']
                else:
                    day_dict['Hospitalized (cumulative)'] = 0
                if 'total' in day.keys():
                    day_dict['Test performed'] = day['total']
                else:
                    day_dict['Test performed'] = 0
                if day['state'] in states_dict.keys():
                    day_dict['Total population'] = states_dict[day['state']]
                else:
                    day_dict['Total population'] = 'NULL'
                to_master.append(day_dict)
            count += 1
    df = pd.DataFrame(to_master)
    df.to_csv('data.csv')

def main():
    get_data()


if __name__ == "__main__":
    main()

