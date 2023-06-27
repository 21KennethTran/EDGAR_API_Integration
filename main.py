from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime

# Showcase functions: get latest filing of company,
# print Y/N info onto Google Sheets given some parameters using web scraper

# Edgar API (< 10 calls / second), RSS feed, Yahoo/Google finance API, Google sheet API
# PARAMS:
#CMP: company market capitalization
#DocType: document type
#DocContents: what key words should be in the document (dict?)
#tradeVolume: trading volume on 30 day average
# runs continuously and responds in real-time

try:
  url = 'https://www.sec.gov/files/company_tickers.json'
  header = {'User-Agent': 'kenpt03@gmail.com'}
  response = requests.get( url, headers=header)
  # print(response.json()['0'])

  parseCIK = response.json()['0']['cik_str']

  # unfiltered dataframe with filled CIKs
  data = pd.DataFrame.from_dict(response.json(), orient='index')
  data['cik_str'] = data['cik_str'].astype(str).str.zfill(10)

  samplecik = data[0:1].cik_str[0]
  url2 = f'https://data.sec.gov/submissions/CIK{samplecik}.json'
  filingdata = requests.get(url2, headers=header)


  print(data)

  # use finviz....
except Exception as e:
  print(f'Error {e} has occured')