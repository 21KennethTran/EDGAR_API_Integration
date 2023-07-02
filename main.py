from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime

from getfiles import ContainsKeyWords

# Showcase functions: get latest filing of company,
# print Y/N info onto Google Sheets given some parameters using web scraper

# Edgar API (< 10 calls / second), RSS feed, Yahoo finance API, Google sheet API
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
  data = response.json()
  my_dict = {}

  # json holds mappings of key value pairs, have to use .items()
  for key, comp in data.items():
    my_dict[comp['ticker']] = comp['cik_str']
  # print(my_dict)

  finviz = 'https://finviz.com/screener.ashx?v=111&f=cap_nano,sh_avgvol_u50&ft=4'
  matched = requests.get(finviz, headers=header)
  soup = BeautifulSoup(matched.content, 'html.parser')
  contents = soup.find_all('td', height="10", align="left")

  for content in contents[::5]:
    ticker = content.text
    # print(my_dict[ticker])
    print(ticker)
    docurl = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={my_dict[ticker]}&type=s-3%25&dateb=&owner=exclude&start=0&count=100&output=atom'
    ContainsKeyWords(docurl)


#   data = pd.DataFrame.from_dict(response.json(), orient='index')
#   data['cik_str'] = data['cik_str'].astype(str).str.zfill(10)

#   samplecik = data[0:1].cik_str[0]
#   url2 = f'https://data.sec.gov/submissions/CIK{samplecik}.json'
#   filingdata = requests.get(url2, headers=header)


  # print(data)

  # parse through these pages using tickers from edgar, then print out to sheets
  # use Google sheet API
  # https://finviz.com/screener.ashx?v=111&f=cap_nano,sh_avgvol_u50&ft=4


  # for later use:
  # https://github.com/mcdallas/wallstreet
except Exception as e:
  print(f'Error {e} has occured')