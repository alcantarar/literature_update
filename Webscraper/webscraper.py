# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:06:04 2019
@author: Gary & Ryan
"""

# https://realpython.com/python-web-scraping-practical-introduction/
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import string
import time
import math
import datetime
abstracts = []

from nltk.corpus import stopwords

from webscraper_functions import simple_get, is_good_response
from webscraper_functions import search, fetch_details, search2, get_abstract
from webscraper_functions import string_parse1, string_parse2, clean_str

import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

try:
    data = pd.read_csv('../Data/RYANDATA.csv')
    print('Loading Data')   
    unique_topics = list(data.Topics.unique())
    
    topics = []
    for item in list(data.Topics_split):
        if isinstance(item, str):
            topics_temp = []
            for item2 in item.split('\''):
                if not item2[0] in ['[',',',']']:
                    topics_temp.append(item2)
            topics.append(topics_temp)
        else:
            topics.append('')
    topics_split = topics
    
    titles = list(data.Titles)
    authors = []
    for item in list(data.Authors):
        if isinstance(item, str):
            authors_temp = []
            for item2 in item.split('\''):
                if item2 == '':
                    authors_temp.append('')
                else:
                    if not item2[0] in ['[',',',']']:
                        authors_temp.append(item2)
            authors.append(authors_temp)
        else:
            authors.append('')
    journals  = list(data.Journals)
    years     = list(data.Journals)
    vol_isus  = list(data.Vol_Isue)
    dois      = list(data.DOI)
    abstracts = list(data.Abstract)
    loaded_data = 1
except:
    print('No Data Found, Analyzing Everything')    
    unique_topics = []
    topics = []
    titles = []
    authors = []
    links = []
    journals = []
    years = []
    vol_isus = []
    dois = []

first_annoying = '12-30-2010'
first_missing_asterisks = '06-16-2010'
first_annoying_time = time.mktime(datetime.datetime.strptime(first_annoying, '%m-%d-%Y').timetuple())
first_missing_asterisks_time = time.mktime(datetime.datetime.strptime(first_missing_asterisks, '%m-%d-%Y').timetuple())
#07-27-2007
jinger_date = '07-19-2007'
jinger_post_time = time.mktime(datetime.datetime.strptime(jinger_date, '%m-%d-%Y').timetuple())


str_punc = ''.join(list(string.punctuation)[0:14]) + ''.join(list(string.punctuation)[15:])
translator = str.maketrans(str_punc, ' '*len(str_punc))

# Make the Stop Words for string cleaning
import string
stop = list(stopwords.words('english'))
stop_c = [string.capwords(word) for word in stop]
for word in stop_c:
    stop.append(word)
new_stop = ['StringElement','NlmCategory','Label','attributes','INTRODUCTION','METHODS','BACKGROUND','RESULTS','CONCLUSIONS']
for item in new_stop:
    stop.append(item)

already_analysed_page = 0
for page in np.arange(0,38):
    already_analyzed_thread = 0
    
    raw_html = simple_get('https://biomch-l.isbweb.org/forums/7-Literature-Update/page'+str(page))
    html = BeautifulSoup(raw_html, 'html.parser')
            
    main_url = 'https://biomch-l.isbweb.org/'
    thread = []
    for a in  html.find_all('a', href=True, id=True):
        if a['href'].find('LITERATURE-UPDATE')>0:
            thread.append(main_url + a['href'][0:a['href'].find('?s')] + '.html')
        if a['href'].find('Literature-Update-(')>0:
            thread.append(main_url + a['href'][0:a['href'].find('?s')] + '.html')
        if a['href'].find('Literature-Update?s')>0:
            thread.append(main_url + a['href'][0:a['href'].find('?s')] + '.html')
        if a['href'].find('literature-update')>0:
            thread.append(main_url + a['href'][0:a['href'].find('?s')] + '.html')
    
    for url in thread:
        time.sleep(.1)
        already_analyzed_inthread = 0
        parse_date =  url[url.find('UPDATE')+7:len(url)-5]
        print('Parsing Page: ' + str(page) + ', Thread: ' + parse_date)
        lit_update = simple_get(url)
        lit_update = BeautifulSoup(lit_update,'html.parser')
        
        for item in lit_update.select('span'):
            if 'class=\"date\"' in str(item):
                indx = str(item).find('class=\"date\"')
                if str(item)[indx+13:indx+18]=='Today' or str(item)[indx+13:indx+22]=='Yesterday':
                    post_time = time.time()
                else:
                    post_date = str(item)[indx+13:indx+23]
                    post_time = time.mktime(datetime.datetime.strptime(post_date, '%m-%d-%Y').timetuple())
                break
        lit_str = lit_update.select('blockquote')[0].text
        
        lit_list = lit_str.split('\n')
        if post_time > first_missing_asterisks_time:
            already_added_titles = 0
            for entry in lit_list:
                if len(entry)>0 and entry[0] == '*' and not entry[0:3] == '***':
                    cur_topic = entry[1:entry[1:].find('*')+1].replace(' ','')
                    cur_topics = cur_topic.split('/')
                    for item in cur_topics:
                        if item not in unique_topics:
                            unique_topics.append(item)                            
#                    if not cur_topic in unique_topics:
#                        unique_topics.append(set(x for l in cur_topic.split('/') for x in l))
                elif len(entry) > 200:
                    topic_temp, author_temp, title_temp, journal_temp, year_temp, vol_isu_temp, doi_temp = string_parse1(entry,cur_topic)
                    if not isinstance(title_temp,str):
                        raise Exception('The parsed title is not a string. Url: '+url+'. Entry: '+entry)
                    if len(title_temp)<5:
                        raise Exception('The parsed title length is less than 5. Url: '+url+'. Entry: '+entry)
                    if title_temp not in titles:
                        topics.append(topic_temp.split('/'))
                        authors.append(author_temp)
                        titles.append(title_temp)
                        journals.append(journal_temp)
                        years.append(year_temp)
                        vol_isus.append(vol_isu_temp)
                        dois.append(doi_temp)
                        try:
                            abstracts.append(clean_str(str(get_abstract(title_temp,doi_temp)),stop))#
                        except:
                            abstracts.append('')
                    else:
                        # print('Title In CSV already')
                        already_added_titles += 1
                        if already_added_titles >= 10:
                            print('Already analyzed thread, skipping')
                            already_analyzed_inthread += 1
                            break
        elif post_time > jinger_post_time:
            cur_topic == []
            entry_temp = ''
            n_combines = 0
            found_first_topics = 0
            entry2 = []
            already_added_titles = 0
            for k, entry in enumerate(lit_list):
                found_topics = 0
                if len(entry.translate(translator).replace(' ',''))>2:
                    for item in entry.translate(translator).replace(' ','').split('/'):
                        if item in unique_topics:
                            found_topics += 1
                        else:
                            break
                    if len(entry.translate(translator).replace(' ','').split('/')) == found_topics:
                        found_topics = 1
                        found_first_topics = 1
                        cur_topic = entry.translate(translator).replace(' ','').split('/')
                if len(entry)>20 and found_first_topics and not found_topics:
                    entry_temp = entry_temp + str(entry) + ' '
                    row_after_topic = 0
                    n_combines += 1
                elif entry == '' and n_combines >=2 and not found_topics:
                    topic_temp, author_temp, title_temp, journal_temp, year_temp, vol_isu_temp, doi_temp = string_parse2(entry_temp,cur_topic)
                    if title_temp not in titles:
                        entry2.append(entry_temp)
                        topics.append(topic_temp)
                        authors.append(author_temp)
                        titles.append(title_temp)
                        journals.append(journal_temp)
                        years.append(year_temp)
                        vol_isus.append(vol_isu_temp)
                        dois.append(doi_temp)
                        try:
                            abstracts.append(clean_str(str(get_abstract(title_temp,doi_temp)),stop))#
                        except:
                            abstracts.append('')
                    else:
                        print('Title In CSV already')
                        already_added_titles += 1
                        if already_added_titles >= 10:
                            already_analyzed_thread += 1
                            break
                    entry_temp = ''
                    n_combines = 0
        else:
            print('Post after Jinger, skpping')
        if already_analyzed_thread > 3:
            already_analysed_page += 1
            print('Already Analyzed Page, going to next')
            break
    if already_analysed_page > 5:
        print('Already analyzed 5 pages, ending parsing')
        break

#========================= Put it together ====================================
#if not loaded_data:
topics_split = topics
topics = ['/'.join(item) for item in topics_split]
data = pd.DataFrame(data = {'Topics_split': topics_split,
                            'Topics': topics,
                            'Authors': authors,
                            'Titles': titles,
                            'Journals': journals,
                            'Years': years,
                            'Vol_Isue': vol_isus,
                            'DOI':dois,
                            'Abstract': abstracts})

data.to_csv('../Data/RYANDATA.csv')