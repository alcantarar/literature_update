# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:06:04 2019

@author: Gary
"""

# https://realpython.com/python-web-scraping-practical-introduction/
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import ast

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
    
try:
    data = pd.read_csv('RYANDATA.csv')
    print('Loading Data')   
    unique_catagories = list(data.Catagory.unique())
    catagories = list(data.Catagory)
    titles = list(data.Titles)
    authors = list(data.Authors)
    journals = list(data.Journals)
    years = list(data.Journals)
    vol_isu = list(data.Vol_Isue)
    doi = list(data.DOI)
except:
    print('No Data Found, Analyzing Everything')    
    unique_catagories = []
    catagories = []
    titles = []
    authors = []
    links = []
    journals = []
    years = []
    vol_isu = []
    doi = []

for page in np.arange(1,22):
    already_analyzed_thread = 0
    
    raw_html = simple_get('https://biomch-l.isbweb.org/forums/7-Literature-Update/page'+str(page))
    html = BeautifulSoup(raw_html, 'html.parser')
            
    main_url = 'https://biomch-l.isbweb.org/'
    thread = []
    for a in  html.find_all('a', href=True, id=True):
        if a['href'].find('LITERATURE-UPDATE')>0:
            thread.append(main_url + a['href'][0:a['href'].find('?s')] + '.html')
    
    for url in thread:
        already_analyzed_inthread = 0
        parse_date =  url[url.find('UPDATE')+7:len(url)-5]
        print('Parsing Page: ' + str(page) + ', Thread: ' + parse_date)
        lit_update = simple_get(url)
        lit_update = BeautifulSoup(lit_update,'html.parser')
        
        lit_str = lit_update.select('blockquote')[0].text
        
        lit_list = lit_str.split('\n')
        for entry in lit_list:
            if len(entry)>0 and entry[0] is '*':
                cur_cat = entry[1:entry[1:].find('*')+1].replace(' ','')
                if not cur_cat in unique_catagories:
                    unique_catagories.append(cur_cat)
            elif len(entry) > 200:
                
                if entry[0:10] == 'http://dx.':
                    entry = entry[entry.find(' ')+1:]
                    
                author = entry[0:entry.find('.')].split(';')                
                authors_temp = [author[1:] if author[0]== ' ' else author for author in author]
                
                entry   = entry[entry.find('.')+2:]
                titles_temp = (entry[0:entry.find('.')])
                entry   = entry[entry.find('.')+2:]
                
                if not titles_temp in titles:
                    authors.append(authors_temp)
                    titles.append(titles.temp)
                    catagories.append(cur_cat)
                    try:
                        year_nan = entry.find('NaN')
                        if year_nan == -1:
                            year_nan = 1000000
                        year_start = min(entry.find('20'),year_nan)
                        journals.append(entry[0:year_start-1])
                        entry   = entry[year_start:]
                        if entry[0:3] == 'NaN':
                            years.append('NaN')
                        else:
                            years.append(entry[0:entry.find(';')])
                        entry   = entry[entry.find(';')+1:]
                        if entry[0:3] == 'NaN':
                            vol_isu.append('NaN')
                        else:
                            vol_isu.append(entry[0:entry.find('.')])
                        doi.append(entry[entry.find('.')+2:])
                    except:
                        journals.append(entry)
                        years.append('NaN')
                        vol_isu.append('NaN')
                        doi.append('NaN')
                else:
                    already_analyzed_inthread += 1
                    if already_analyzed_inthread > 5:
#                        print('Already Analyzed Thread, going to next')
                        already_analyzed_thread += 1
                        break
        if already_analyzed_thread > 3:
#            print('Already Analyzed Page, going to next')
            break
                

data = pd.DataFrame(data = {'Catagory': catagories,
                            'Authors': authors,
                            'Titles': titles,
                            'Journals': journals,
                            'Years': years,
                            'Vol_Isue': vol_isu,
                            'DOI':doi})

data.to_csv('RYANDATA.csv')

cat = []
cat_len = []
for k in np.arange(len(data['Catagory'].unique())):
    cat.append(data['Catagory'].unique()[k])
    cat_len.append(len(data[data.Catagory==cat[k]]))

cat_lengths = pd.DataFrame(data = {'Catagory': cat,
                                   'Length': cat_len})
min_num = len(catagories)*.01
cat_lengths = cat_lengths.query('Length>' + str(min_num))

filtered_data = pd.DataFrame(data =  {'Catagory': [],
                                      'Authors': [],
                                      'Titles': [],
                                      'Journals': [],
                                      'Years': [],
                                      'Vol_Isue': [],
                                      'DOI': []})

for cat in cat_lengths.Catagory.unique():
    filtered_data = pd.concat([filtered_data,data[data.Catagory==cat and data]])

filtered_data.to_csv('RYANDATA_filt.csv')














