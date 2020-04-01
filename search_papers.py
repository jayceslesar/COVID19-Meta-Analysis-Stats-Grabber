import Daily_Article_Sweep
import re
import requests
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



papers = Daily_Article_Sweep.Daily_Article_Sweep().todays_data_df
print(papers.head)
