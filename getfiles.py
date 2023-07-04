from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime

# More formal function to **find** most recent filing of a company given its company identifier key, type of filing, and filing format
# Alternative to naive.py
#PARAMS:
# CIK - positive integer number reprsenting the company's ID under Edgar
# format - string representing format of data to receive; (.xml, .htm ...)
# filing - string representing type of filing to receive; (10-K, etc.)
#RETURN: most recent filing of specified company in specified format

def getCompanyFilings(cik="0001318605", format=".xml", filing="10-K"):
    try:
        url = f'https://data.sec.gov/submissions/CIK{CIK}.json'
        header = {'User-Agent': 'kenpt03@gmail.com'}
        response = requests.get(url, headers=header)
        data = json.loads(response.text)

        first = 0
        for eck in data['filings']['recent']['primaryDocDescription']:
            if filing in eck:
                break
        first += 1

        # url of first filing instance in form of date (.htm)
        file10k = data['filings']['recent']['primaryDocument'][first]
        # filer ID
        acc = data['filings']['recent']['accessionNumber'][first]
        acc = acc.replace("-", "")

        url10k = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc}/{file10k}"
        print(url10k)

        # print xml version of report
        file10kxml = file10k.replace(".","_") + format
        urlf = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc}/{file10kxml}"
        return urlf
    except Exception as e:
        print(f'Error {e} has occured')

# Function to find if a company's first s-3 filing contains all of the specified key words.
# TO DO: use some finance API to find trading volume over 30 day average (not 3 month)


#PARAMS:
# url: string url of all specified filings of a company from edgar
# words: array of strings of key words that must be found in the first filing of this document type
#RETURN: T/F if key words are found in file\\drive\\1VM9vVpf5zItbskcyQUB0CPfIoYuLgnfP
def ContainsKeyWords(url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=s-3%25&dateb=&owner=exclude&start=0&count=100&output=atom", words=["Common Shares", "Preferred Shares", "Warrants"]):
    try:
        header = {'User-Agent': 'kenpt03@gmail.com'}
        while url is not None:
            response = requests.get(url, headers=header)
            soup = BeautifulSoup(response.content, 'xml')

            links = soup.find_all('link', href=True, rel='next')
            if len(links) == 0:
                break
            url = links[0]['href']

        # response = requests.get(url, headers=header)
        # soup = BeautifulSoup(response.content, 'xml')

        keydata = ['', '']
        
        if len(soup.find_all('entry')) == 0:
            # print("no file")
            keydata = ['no file', 'No']
            return keydata
        keydata[0] = 'Yes'
        ent = soup.find_all('entry')[-1].find('filing-href').text

        href = requests.get(ent, headers=header)

        soup2 = BeautifulSoup(href.content, 'html.parser')
        file = soup2.find_all('tr')[-1].find('a')['href']
        file = f"https://www.sec.gov/{file}"

        parser = requests.get(file, headers=header)

        # word printed before Yes is the word not found
        keyfound = True
        content = parser.text
        for word in words:
        # print(word)
            if word not in content:
                keyfound = False
                break

        if keyfound:
            # print('Yes')
            keydata[1] = 'Yes'
            return keydata
        else:
            # print('No')
            keydata[1] = 'No'
            return keydata

    except Exception as e:
        print(f'Error {e} has occurred')


ContainsKeyWords()