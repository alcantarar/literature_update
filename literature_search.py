#==============================================================================
#=========================  Define the search criteria ========================

from Bio import Entrez
import numpy as np

def search(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='most recent', 
                            retmax='5000',
                            retmode='xml', 
                            datetype = 'pdat',
                            reldate = 7, #only within n days from now
#                             mindate = '2019/03/25',
#                             maxdate = '2019/03/27', #for searching date range
                            term=query)
    results = Entrez.read(handle)
    return results

#search terms (can test string with Pubmed Advanced Search)
search_results = search('(Biomech*[Title/Abstract] OR locomot*[Title/Abstract])')

#==============================================================================
#========================= Perform Search and Save Paper Titles ===============
def fetch_details(id_list):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=id_list)
    results = Entrez.read(handle)
    return results

id_list = search_results['IdList']
papers = fetch_details(id_list)
print("")

# Definitely could change these loops for speed.
papers_length = len(papers['PubmedArticle'])
titles = [None]*papers_length
full_titles = [None]*papers_length
keywords = [None]*papers_length
authors = [None]*papers_length
links = [None]*papers_length
journals = [None]*papers_length
abstracts = [None]*papers_length

def clean_str(abs_string,stop):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    abs_string = abs_string.translate(translator)
    abs_string = abs_string.split()
    abs_string = [word for word in abs_string if word not in stop]
    abs_string = ' '.join(abs_string)
    return abs_string

# Make the Stop Words for string cleaning
from nltk.corpus import stopwords
import string
stop = list(stopwords.words('english'))
stop_c = [string.capwords(word) for word in stop]
for word in stop_c:
    stop.append(word)
new_stop = ['StringElement','NlmCategory','Label','attributes',
            'INTRODUCTION','METHODS','BACKGROUND','RESULTS',
            'CONCLUSIONS','study','results',
            'significant','purpose', 'significantly','increased',
            'showed','conclusion']
for item in new_stop:
    stop.append(item)

for i, paper in enumerate(papers['PubmedArticle']):
    titles[i] = clean_str(papers['PubmedArticle'][i]['MedlineCitation']['Article']['ArticleTitle'],stop)
    full_titles[i] = papers['PubmedArticle'][i]['MedlineCitation']['Article']['ArticleTitle']
    try:
        abstracts[i] = clean_str(papers['PubmedArticle'][i]['MedlineCitation']['Article']['Abstract']['AbstractText'][0],stop)  
    except:
        abstracts[i] = ''
print(np.size(titles),'Papers found')

#==============================================================================
#========================= Pull information from PubMed Results ===============
#### Format title, journal, authors in markdown friendly manner

for i, paper in enumerate(papers['PubmedArticle']):
    if paper['MedlineCitation']['Article']['ArticleTitle'] == '':
        continue
    if paper['MedlineCitation']['Article']['ArticleTitle'][0] == '[':
        links[i] = "* [%s](https://www.ncbi.nlm.nih.gov/pubmed/%s)" % \
            (paper['MedlineCitation']['Article']['ArticleTitle'][1:-1],
             paper['MedlineCitation']['PMID'])
    else:
        links[i] = "* [%s](https://www.ncbi.nlm.nih.gov/pubmed/%s)" % \
            (paper['MedlineCitation']['Article']['ArticleTitle'],
             paper['MedlineCitation']['PMID'])
        
    auths = []
    try:
        for auth in paper['MedlineCitation']['Article']['AuthorList']:
            try:
                auth_name = [auth['LastName'],auth['Initials']+',']
                auth_name = ' '.join(auth_name)
                auths.append(auth_name)
            except:
                auths.append('')
                print(paper['MedlineCitation']['Article']['ArticleTitle'],
                      'has an issue with an author name')
    except:
        auths.append('AUTHOR NAMES ERROR')
        print(paper['MedlineCitation']['Article']['ArticleTitle'],'has no author list?')
    authors[i] = ' '.join(auths)
    journals[i] = '*%s*' % (paper['MedlineCitation']['Article']['Journal']['Title']) 
    # store keywords 
    if paper['MedlineCitation']['KeywordList'] != []:
        kwds = []
        for kw in paper['MedlineCitation']['KeywordList'][0]:
            kwds.append(kw[:])         
        keywords[i] = ' '.join(kwds)
        
#==============================================================================
#========================= Clean up title and word strings ====================

titles = [t.lower() for t in titles] #same case
titles = [t.replace('<sub>',' ').replace('</sub>','') for t in titles] #subscript
titles = [t.replace('<i>',' ').replace('</i>','') for t in titles] #italics
titles = [t.replace('[','').replace(']','') for t in titles] #remove brackets from html parser
#clean up keywords
keywords2 = []
for k in keywords:
    if k is None:
        keywords2.append('')
    else:
        keywords2.append(k.lower())
keywords = keywords2
#keywords = [k.lower() for k in keywords] #same case

#==============================================================================
#========================= Loading the things =================================

# Load Top-performing Model
from keras.models import load_model
model = load_model('Models/Keras_model/model_DNN.h5')
print('\nLoaded model from disk')

# Load Associated Vectorizer
from sklearn.externals import joblib #pickle.load throws warning.
from sklearn.preprocessing import LabelEncoder
#load vectorizer and label encoder
vect = joblib.load(open('Models/Keras_model/Vectorizer_tdif.pkl','rb'))
le = LabelEncoder()
le.classes_   = np.load('Models/Keras_model/LabelEncoder.npy')
print('\nLoaded Vectorizer')

#==============================================================================
#========================= Vectorize Strings ==================================
#get titles for this week's literature update
import pandas as pd
papers_df = pd.DataFrame({'title': titles,
                          'keywords': keywords,
                          'abstract': abstracts,
                          'author': authors,
                          'journal': journals})

for index, row in papers_df.iterrows():
    if row['abstract'] == '' or row['author'] == 'AUTHOR NAMES ERROR' or row['title'] == '':
        papers_df.drop(index,inplace=True)

#join titles, keywords, and abstract
papers_df['everything'] = pd.DataFrame(papers_df['title'].astype(str)*4+\
                                       papers_df['abstract'].astype(str)+\
                                       papers_df['keywords'].astype(str))

titles_vec = vect.transform(papers_df['everything'])
# OR if you don't want to use just the title:
# titles_vec = vect.transform(papers_df['title'])

#==============================================================================
#========================= Predict topics =====================================
# Predict Topics For Each Paper
prediction_vec = model.predict(titles_vec)

topics       = []
pred_val     = []
pred_val_vec = []
title_temp   = []
indx         = []

for k, top_val in enumerate(prediction_vec):
    if k in papers_df.index:
        papers_df.loc[k,:]
        pred_val = np.max(top_val)
#        if pred_val > 0*np.sort(top_val)[-2]:
        indx.append(k)
        topics.append(le.inverse_transform([np.argmax(top_val)])[0])
        title_temp.append(papers_df['title'][k])
        pred_val_vec.append(pred_val*100)
#        else:
#            indx.append(k)
#            topics.append('unknown')
#            title_temp.append(papers_df['title'][k])
    else:
        print('Skipping prediction of paper #: ' + str(k))
papers_df = pd.DataFrame(data = {'title': title_temp,
                                  'topic': topics,
                                  'pred_val': pred_val_vec})

#==============================================================================
#========================= Save Titles and Topics =============================

#add info for github markdown format
papers_df['title']      = [title if title[1] is not '[' else title[1:-1] for title in papers_df['title']]
papers_df['authors']    = [authors[k] if authors[k][1] is not '[' else authors[1:-1] for k in indx]
papers_df['journal']    = [journals[k] for k in indx]
papers_df['links']      = [links[k] for k in indx]
papers_df['full_title'] = [full_titles[k] for k in indx]
#generate filename
import datetime
now = datetime.datetime.now()
strings = [str(now.year), str(now.month), str(now.day),'litupdate.csv']
fname = 'Literature_Updates/'+'-'.join(strings)
strings = [str(now.year), str(now.month), str(now.day),'litupdate.md']
mdname = 'Literature_Updates/'+'-'.join(strings)
strings = [str(now.year), str(now.month), str(now.day),'litupdate']
urlname = '-'.join(strings)

print('Filename: ',fname)

# Compare to previously searched papers
#old_papers = pd.concat([pd.read_csv('Literature_Updates/2019-5-7-litupdate.csv'),
#                        pd.read_csv('Literature_Updates/2019-4-30-litupdate.csv')])
compare_papers = pd.read_csv('Literature_Updates/compare_papers.csv')

# Probably Don't need to compare against training data, could remove for speed?
trained_papers = pd.read_csv('Data/RYANDATA.csv')
trained_papers.columns = ['number',
                          'topics_split',
                          'topic',
                          'authors',
                          'title',
                          'Journals',
                          'Years',
                          'Vol_Isue',
                          'DOI',
                          'abstract']
trained_papers.drop(['topics_split','number'],axis=1)

full_title = []
for item in compare_papers.links:
    full_title.append(item.replace('[',';').replace(']',';').split(';')[1])
compare_papers['full_title'] = full_title

for index, row in papers_df.iterrows():
    if row['full_title'] in list(compare_papers['full_title'])\
    or row['full_title'] in list(trained_papers['title']):
        papers_df.drop(index,inplace=True)
    else:
        compare_papers.append(row)

with open('Literature_Updates/compare_papers.csv', 'w', encoding = 'utf-8', newline = '') as f:
    compare_papers.to_csv(f, header=True, index = False)  

papers_df.sort_values('topic').to_csv(fname, index = False)
print('\nLiterature Update Exported as .csv')

# Compile papers grouped by topic
md_file = open(mdname, 'w', encoding = 'utf-8')
md_file.write('---\n')
md_file.write('layout: single\n')
md_file.write('title: Biomechanics Literature Update\n')
md_file.write('collection: literature\n')
md_file.write('permalink: /literature/%s\n' % urlname)
md_file.write('excerpt: <br>\n')
md_file.write('toc: true\n')
md_file.write('toc_sticky: true\n')
md_file.write('toc_label: Topics\n')
md_file.write('---\n')

#tidy up topic strings
topic_list = np.unique(papers_df.sort_values('topic')['topic'])
ss = [s for s in topic_list if 'UNIQUE' in s]
for i,t in enumerate(topic_list):
    if 'UNIQUE' in t:  
        topic_list[i] = 'UNIQUE TOPIC'
        print('Assigned unique topic: ' + str(i))
    if 'IMPACT' in t:
        topic_list[i] = 'TRAUMA/IMPACT'

#==============================================================================
#========================= Make Markdown File =================================
st = '### Created by: [Ryan Alcantara](https://twitter.com/Ryan_Alcantara_)'
st = st + ' & [Gary Bruening](https://twitter.com/garebearbru) -'
st = st + ' University of Colorado Boulder\n\n'
md_file.write(st)
for topic in topic_list:
    md_file.write('----\n')
    md_file.write('# %s\n' % topic)
    md_file.write('----\n')
    md_file.write('\n')
    md_file.write('[Back to top](#created-by-ryan-alcantara--gary-bruening---university-of-colorado-boulder)')
    md_file.write('\n')
    papers_subset = pd.DataFrame(papers_df[papers_df.topic == topic].reset_index(drop = True))
    for i,paper in enumerate(papers_subset['links']):
        md_file.write('%s\n' % paper)
        md_file.write('%s\n' % papers_subset['authors'][i])
        md_file.write('%s.  \n' % papers_subset['journal'][i])
        md_file.write('(%.1f%%) \n' % papers_subset['pred_val'][i])
        md_file.write('\n')

md_file.close()
print('Literature Update Exported as Markdown')
print('Location:',mdname)
