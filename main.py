import requests
from bs4 import BeautifulSoup # scraping XML files
import json
import datetime

# params
# action: (not needed anymore?) By default should be set to getcompany.
# CIK: (required) Is the CIK number of the company you are searching.
# type: (optional) Allows filtering the type of form. For example, if set to 10-k only the 10-K filings are returned.
# dateb: (optional) Will only return the filings before a given date. The format is as follows YYYYMMDD
# owner: (required) Is set to exclude by default and specifies ownership. You may also set it to include and only.
# start: (optional) Is the starting index of the results. For example, if I have 100 results but want to start at 45 of 100, I would pass 45.
# state: (optional) The company's state.
# filenum: (optional) The filing number.
# sic: (optional) The company's SIC (Standard Industry Classification) identifier
# output: (optional) Defines returned data structure as either xml (atom) or normal html.
# count: (optional) The number of results you want to see with your request, the max is 100 and if not set it will default to 40.

# endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"
# param_dict = {'CIK':'0001318605',
#               'type':'10-k',
#               }

url = 'https://data.sec.gov/submissions/CIK0001318605.json'
response = requests.get(url)
data = json.loads(response.text)
print(data)