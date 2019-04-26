# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:14:44 2019

@author: Gary
"""

cur_topic == []
entry_temp = ''
n_combines = 0
found_first_topics = 0
for k, entry in enumerate(lit_list):
#                if entry.translate(translator).replace(' ','') in unique_topics and len(entry.translate(translator).replace(' ',''))>2:
#                    cur_topic = entry.translate(translator).replace(' ','')
#                    row_after_topic = 1                
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
            print('found topics')
    
    print(len(entry),found_first_topics,found_topics)
    if len(entry)>20 and found_first_topics and not found_topics:
        entry_temp = entry_temp + str(entry)
        row_after_topic = 0
        n_combines += 1
    elif entry == '' and n_combines >=2 and not found_topics:
        topic_temp, author_temp, title_temp, journal_temp, year_temp, vol_isu_temp, doi_temp = string_parse2(entry_temp,cur_topic)
        print(topic_temp)
        topics.append(topic_temp)
        authors.append(author_temp)
        titles.append(title_temp)
        journals.append(journal_temp)
        years.append(year_temp)
        dois.append(doi_temp)
        entry_temp = ''
        n_combines = 0