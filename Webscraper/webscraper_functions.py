# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:04:55 2019

@author: Gary
"""

from contextlib import closing
from requests import get
from requests.exceptions import RequestException

from Bio import Entrez
Entrez.api_key = "YOUR API KEY"

import string

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
    
def string_parse1(entry, topic):
    if 'Jones M.L.H., Ebert S.M., Reed M.P..' in entry:
        author  = 'Jones M.L.H., Ebert S.M., Reed M.P.'
        title   = 'Investigating the effect of task parameters on force exertion rating of one-handed pulling tasks. '
        journal = 'Proceedings Of The Human Factors And Ergonomics Society'
        year    = '2018'
        vol_isu = '2:833-837'
        doi     = ''
        return topic, author, title, journal, year, vol_isu, doi

    if entry[0:10] == 'http://dx.':
        entry = entry[entry.find(' ')+1:]
        
    if entry[0:3] == '01. ':
        entry = entry[4:]
    
    if '..' in entry and entry.find('..') < len(entry)-50:
        author = entry[0:entry.find('..')+1].split(',')
        entry = entry[entry.find('..')+3:]
    else:
        author = entry[0:entry.find('.')].split(';')
        entry = entry[entry.find('.')+2:]             
    authors_temp = [author[1:] if author[0]== ' ' else author for author in author]
    
    if entry.find('.') > 20:
        titles_temp = (entry[0:entry.find('.')])
    else:
        titles_temp = entry[0:entry[20:-1].find('.')+20]
    if len(titles_temp)<5:
        entry   = entry[entry.find('.')+2:]
        if entry[0:109] == 'elegans locomotion: finding balance in imbalance. Biochemical And Biophysical Roles Of Cell Surface Molecules':
            titles_temp = entry[0:109]
            entry = entry[109:]
        else:
            titles_temp = (entry[0:entry.find('.')])
            entry = entry[entry.find('.')+2:]
    else:
        entry = entry[entry.find('.')+2:]
    
#    if not titles_temp in titles:
    author = authors_temp
    title = titles_temp
    topic = topic
    try:
        year_nan = entry.find('NaN')
        if year_nan == -1:
            year_nan = 1000000
        year_start = min(entry.find('20'),year_nan)
        journal = entry[0:year_start-1]
        entry = entry[year_start:]
        if entry[0:3] == 'NaN':
            year = 'NaN'
        else:
            year = entry[0:entry.find(';')]
        entry   = entry[entry.find(';')+1:]
        if entry[0:3] == 'NaN':
            vol_isu = 'NaN'
        else:
            vol_isu = entry[0:entry.find('.')]
        doi = entry[entry.find('.')+2:]
    except:
        journal = entry
        year = 'NaN'
        vol_isu = 'NaN'
        doi = 'NaN'
    return topic, author, title, journal, year, vol_isu, doi

def string_parse2(entry, topic):
    if 'Jones M.L.H., Ebert S.M., Reed M.P..' in entry:
        author  = 'Jones M.L.H., Ebert S.M., Reed M.P.'
        title   = 'Investigating the effect of task parameters on force exertion rating of one-handed pulling tasks. '
        journal = 'Proceedings Of The Human Factors And Ergonomics Society'
        year    = '2018'
        vol_isu = '2:833-837'
        doi     = ''
        return topic, author, title, journal, year, vol_isu, doi
    if 'Carey, J, Craig, M, Kerstein, RB, Radke, J,' in entry:
        author  = 'Carey, J, Craig, M, Kerstein, RB, Radke, J,'.split(',')
        title   = 'Determining a relationship between applied occlusal load and articulating paper mark area'
        journal = 'The Open Dentistry Journal'
        year    = '2007'
        vol_isu = '1;1-7'
        doi     = ''
        return topic, author, title, journal, year, vol_isu, doi
    if 'Coulon M, Baudoin C, Depaulis-Carre M, Heyman Y, Renard JP, Richard C' in entry:
        author  = 'Coulon M, Baudoin C, Depaulis-Carre M, Heyman Y, Renard JP, Richard C'.split(',')
        title   = 'Dairy cattle exploratory and social behaviors: Is there an effect of cloning?'
        journal = 'Theriogenology'
        year    = '2007'
        vol_isu = '68(8):1097-103'
        doi     = ''
        return topic, author, title, journal, year, vol_isu, doi
    if entry[0:10] == 'http://dx.':
        entry = entry[entry.find(' ')+1:]
        
    author = entry[0:entry.find('.')].split(',')    
#    print(author)            
    authors_temp = [author[1:] if author[0]== ' ' else author for author in author]
    
    entry   = entry[entry.find('.')+1:]
    titles_temp = (entry[0:entry.find('.')])
    entry   = entry[entry.find('.')+2:]
    
#    if not titles_temp in titles:
    author = authors_temp
    title = titles_temp
    topic = topic
    try:
        year_nan = entry.find('NaN')
        if year_nan == -1:
            year_nan = 1000000
        year_start = min(entry.find('20'),year_nan)
        journal = entry[0:year_start-1]
        entry = entry[year_start:]
        if entry[0:3] == 'NaN':
            year = 'NaN'
        else:
            year = entry[0:entry.find(';')]
        entry   = entry[entry.find(';')+1:]
        if entry[0:3] == 'NaN':
            vol_isu = 'NaN'
        else:
            vol_isu = entry[0:entry.find('.')]
        doi = entry[entry.find('http'):]
    except:
        journal = entry
        year = 'NaN'
        vol_isu = 'NaN'
        doi = 'NaN'
    return topic, author, title, journal, year, vol_isu, doi

#========================= Init Abstract Fucntions ============================
def search(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='most recent', 
                            retmax='5000',
                            retmode='xml', 
                            reldate = 7, #only within n days from now
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

def search2(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed', 
#                            sort='most recent', 
#                            retmax='5000',
#                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results


def get_abstract(title, doi):
    paper = search2(title)
    if paper['IdList'] == []:
#        print('- No Title Match.')# Searching by DOI')
#        time.sleep(.1)
        paper = search2(doi.replace('http://dx.doi.org/',''))
        if paper['IdList'] == []:
#            print('DOI Search Failed')
            return ''
    paper = fetch_details(paper['IdList'])
    title_len = len(title.split())
#    pulled_title_len = len(paper['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'].lower())
    pulled_title = paper['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'].lower()
    intersect_len = len(list(set(title.split()).intersection(pulled_title.split())))
    if intersect_len >= .5*title_len:
#        print('Intersect Found')
        return paper['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText']
    else:
#        print('No intersect, returning \'\'')
        return ''


def clean_str(abs_string,stop):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    abs_string = abs_string.translate(translator)
    abs_string = abs_string.split()
    abs_string = [word for word in abs_string if word not in stop]
    abs_string = ' '.join(abs_string)
    return abs_string
