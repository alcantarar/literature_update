# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:06:04 2019
@author: Gary & Ryan
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
import os

#os.chdir('E:/Google Drive/Documents/BiomechL_webscraper/literature_update

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
    
#try:
data = pd.read_csv('../Data/RYANDATA.csv')
print('Loading Data')   
unique_catagories = list(data.Catagory.unique())
catagories = list(data.Catagory)
titles = list(data.Titles)
authors = list(data.Authors)
journals = list(data.Journals)
years = list(data.Journals)
vol_isu = list(data.Vol_Isue)
doi = list(data.DOI)
abstracts = list(data.Abstract)
#except:
#    print('No Data Found, Analyzing Everything')    
#    unique_catagories = []
#    catagories = []
#    titles = []
#    authors = []
#    links = []
#    journals = []
#    years = []
#    vol_isu = []
#    doi = []

#for page in np.arange(1,22):
#    already_analyzed_thread = 0
#    
#    raw_html = simple_get('https://biomch-l.isbweb.org/forums/7-Literature-Update/page'+str(page))
#    html = BeautifulSoup(raw_html, 'html.parser')
#            
#    main_url = 'https://biomch-l.isbweb.org/'
#    thread = []
#    for a in  html.find_all('a', href=True, id=True):
#        if a['href'].find('LITERATURE-UPDATE')>0:
#            thread.append(main_url + a['href'][0:a['href'].find('?s')] + '.html')
#    
#    for url in thread:
#        already_analyzed_inthread = 0
#        parse_date =  url[url.find('UPDATE')+7:len(url)-5]
#        print('Parsing Page: ' + str(page) + ', Thread: ' + parse_date)
#        lit_update = simple_get(url)
#        lit_update = BeautifulSoup(lit_update,'html.parser')
#        
#        lit_str = lit_update.select('blockquote')[0].text
#        
#        lit_list = lit_str.split('\n')
#        for entry in lit_list:
#            if len(entry)>0 and entry[0] is '*':
#                cur_cat = entry[1:entry[1:].find('*')+1].replace(' ','')
#                if not cur_cat in unique_catagories:
#                    unique_catagories.append(cur_cat)
#            elif len(entry) > 200:
#                
#                if entry[0:10] == 'http://dx.':
#                    entry = entry[entry.find(' ')+1:]
#                    
#                author = entry[0:entry.find('.')].split(';')                
#                authors_temp = [author[1:] if author[0]== ' ' else author for author in author]
#                
#                entry   = entry[entry.find('.')+2:]
#                titles_temp = (entry[0:entry.find('.')])
#                entry   = entry[entry.find('.')+2:]
#                
#                if not titles_temp in titles:
#                    authors.append(authors_temp)
#                    titles.append(titles_temp)
#                    catagories.append(cur_cat)
#                    try:
#                        year_nan = entry.find('NaN')
#                        if year_nan == -1:
#                            year_nan = 1000000
#                        year_start = min(entry.find('20'),year_nan)
#                        journals.append(entry[0:year_start-1])
#                        entry   = entry[year_start:]
#                        if entry[0:3] == 'NaN':
#                            years.append('NaN')
#                        else:
#                            years.append(entry[0:entry.find(';')])
#                        entry   = entry[entry.find(';')+1:]
#                        if entry[0:3] == 'NaN':
#                            vol_isu.append('NaN')
#                        else:
#                            vol_isu.append(entry[0:entry.find('.')])
#                        doi.append(entry[entry.find('.')+2:])
#                    except:
#                        journals.append(entry)
#                        years.append('NaN')
#                        vol_isu.append('NaN')
#                        doi.append('NaN')
#                else:
#                    already_analyzed_inthread += 1
#                    if already_analyzed_inthread > 5:
##                        print('Already Analyzed Thread, going to next')
#                        already_analyzed_thread += 1
#                        break
#        if already_analyzed_thread > 3:
##            print('Already Analyzed Page, going to next')
#            break
                

##========================= Getting Abstracts ==================================
#from Bio import Entrez
#import numpy as np
#Entrez.api_key = "f3e4ca963cb5371b03e53e49ca9b836f2c08"
#
#def search(query):
#    Entrez.email = 'your.email@example.com'
#    handle = Entrez.esearch(db='pubmed', 
#                            sort='most recent', 
#                            retmax='5000',
#                            retmode='xml', 
#                            reldate = 7, #only within n days from now
#                            term=query)
#    results = Entrez.read(handle)
#    return results
#
#def fetch_details(id_list):
#    ids = ','.join(id_list)
#    Entrez.email = 'your.email@example.com'
#    handle = Entrez.efetch(db='pubmed',
#                           retmode='xml',
#                           id=ids)
#    results = Entrez.read(handle)
#    return results
#
#def search2(query):
#    Entrez.email = 'your.email@example.com'
#    handle = Entrez.esearch(db='pubmed', 
##                            sort='most recent', 
##                            retmax='5000',
##                            retmode='xml', 
#                            term=query)
#    results = Entrez.read(handle)
#    return results
#
#import time
#abstracts = []
#
#def get_abstract(title, doi):
#    paper = search2(title)
#    if paper['IdList'] == []:
#        print('- No Title Match.')# Searching by DOI')
#        time.sleep(.1)
#        paper = search2(doi.replace('http://dx.doi.org/',''))
#        if paper['IdList'] == []:
#            print('DOI Search Failed')
#            return ''
#    paper = fetch_details(paper['IdList'])
#    title_len = len(title.split())
##    pulled_title_len = len(paper['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'].lower())
#    pulled_title = paper['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'].lower()
#    intersect_len = len(list(set(title.split()).intersection(pulled_title.split())))
#    if intersect_len >= .5*title_len:
##        print('Intersect Found')
#        return paper['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText']
#    else:
#        print('No intersect, returning \'\'')
#        return ''
#
#from nltk.corpus import stopwords
#
#def clean_str(abs_string,stop):
#    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
#    abs_string = abs_string.translate(translator)
#    abs_string = abs_string.split()
#    abs_string = [word for word in abs_string if word not in stop]
#    abs_string = ' '.join(abs_string)
#    return abs_string
#    
## Make the Stop Words
#import string
#stop = list(stopwords.words('english'))
#stop_c = [string.capwords(word) for word in stop]
#for word in stop_c:
#    stop.append(word)
#new_stop = ['StringElement','NlmCategory','Label','attributes','INTRODUCTION','METHODS','BACKGROUND','RESULTS','CONCLUSIONS']
#for item in new_stop:
#    stop.append(item)
#
## Pull Abstracts
#abstracts = []
#toc = time.perf_counter()
#tic = time.perf_counter()
#for i, title in enumerate(titles):
##    if i % 10 == 0:
#    print('Analyzing Title: '+ str(i))
#    if toc - tic < .1:
#        time.sleep(.1 - (toc-tic))
#        print('Sleeping a sec')
#    tic = time.perf_counter()
#    try:
#        abstracts.append(clean_str(str(get_abstract(title,doi[i])),stop))#
#    except:
#        abstracts.append('')
#    toc = time.perf_counter()
    
#========================= Put it together ====================================
data = pd.DataFrame(data = {'Catagory': catagories,
                            'Authors': authors,
                            'Titles': titles,
                            'Journals': journals,
                            'Years': years,
                            'Vol_Isue': vol_isu,
                            'DOI':doi,
                            'Abstract': abstracts})

data.to_csv('../Data/RYANDATA.csv')

cat = []
cat_len = []
for k in np.arange(len(data['Catagory'].unique())):
    cat.append(data['Catagory'].unique()[k])
    cat_len.append(len(data[data.Catagory==cat[k]]))

cat_lengths = pd.DataFrame(data = {'Catagory': cat,
                                   'Length': cat_len})
min_num = len(catagories)*.05
min_num = 500
cat_lengths = cat_lengths.query('Length>' + str(min_num))

filtered_data = pd.DataFrame(data =  {'Catagory': [],
                                      'Authors': [],
                                      'Titles': [],
                                      'Journals': [],
                                      'Years': [],
                                      'Vol_Isue': [],
                                      'DOI': [],
                                      'Abstract': []})

for cat in cat_lengths.Catagory.unique():
    if not cat == 'UNIQUETOPIC':
        filtered_data = pd.concat([filtered_data,data[data.Catagory==cat]])

filtered_data.to_csv('../Data/RYANDATA_filt.csv')

filtered_data = filtered_data.groupby('Catagory').apply(lambda s: s.sample(500))
filtered_data.to_csv('../Data/RYANDATA_filt_even.csv')

# %% Test
    
#Some papers just don't have an abstact: 
#titles[9]  = https://www.ncbi.nlm.nih.gov/pubmed/?term=Accumulation+of+microdamage+at+complete+and+incomplete+fracture+sites+in+a+patient+with+bilateral+atypical+femoral+fractures+on+glucocorticoid+and+bisphosphonate+therapy 
    
#test = get_abstract(titles[84], doi[84])
#test = str(test)
#translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
#test = test.translate(translator)
#test = test.split()
#test = [word for word in test if word not in stop]
#test = ' '.join(test)

#num_blank = 0
#for item in abstract['abstract']:
#    if item == '[]':
#        num_blank += 1





