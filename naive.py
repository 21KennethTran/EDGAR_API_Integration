from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup # scraping XML files
import json
import datetime

# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36

try:
  CIK = '0001318605' # TSLA's identifier
  url = f'https://data.sec.gov/submissions/CIK{CIK}.json'
  header = {'User-Agent': 'Mozilla/5.0'}
  response = requests.get(url, headers=header)
  data = json.loads(response.text)

  # print(len(data))
  # for bleh in data['filings']['recent']:
  #   print(bleh)

  first10k = 0
  for eck in data['filings']['recent']['primaryDocDescription']:
    if "10-K" in eck:
      break
    first10k += 1

  # url of first 10-k instance in form of date (.htm)
  file10k = data['filings']['recent']['primaryDocument'][first10k]
  # filer ID
  acc = data['filings']['recent']['accessionNumber'][first10k]
  acc = acc.replace("-", "")

  # print(acc)
  # print(file10k)
  # print(len(data['filings']['recent']['primaryDocDescription']))
  # print(len(data['filings']['recent']['primaryDocument']))

  url10k = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc}/{file10k}"
  # url10k = "https://www.sec.gov/Archives/edgar/data/0001318605/000095017023001409/tsla-20221231.htm"
  # req = Request(url10k, headers=header)
  # urlopen(req)
  print(url10k)


  # PARAMS to consider:
  # CIK -> company ID
  # link format -> htm, xsd, _cal.xml . . . htm is most consistent
  # filing -> 10-k 8-k, etc.

  # return url10k
except Exception as e:
  print(f'Error {e} has occured')