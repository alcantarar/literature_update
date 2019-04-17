for page in np.arange(1,2):
    already_analyzed_inpage = 0
    
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
                else:
                    already_analyzed_inthread += 1
                    if already_analyzed_inthread > 5:
                        print('Already Analyzed Thread, going to next')
                        already_analyzed_inpage += 1
                        break
        if already_analyzed_inpage > 3:
            print('Already Analyzed Page, going to next')
            break