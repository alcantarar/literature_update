from Bio import Entrez
import numpy as np

def search(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='most recent', 
                            retmax='30',
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

search_results = search('(biomech*[Title/Abstract] OR locomot*[Title/Abstract]) AND bone*[Title/Abstract] NOT mice NOT fish NOT bird NOT rat NOT zoo')
id_list = search_results['IdList']
papers = fetch_details(id_list)
print("")
for i, paper in enumerate(papers['PubmedArticle']):
    print("* [%s](https://www.ncbi.nlm.nih.gov/pubmed/%s)" % (paper['MedlineCitation']['Article']['ArticleTitle'],paper['MedlineCitation']['PMID']))
    for auth in np.arange(1,np.size(paper['MedlineCitation']['Article']['AuthorList'])):
        print("%s %s," % (paper['MedlineCitation']['Article']['AuthorList'][auth]['LastName'],paper['MedlineCitation']['Article']['AuthorList'][auth]['Initials']))
    print('%s' % (paper['MedlineCitation']['Article']['Journal']['Title']) )
    # #store keywords 
    # print("----")
    # if paper['MedlineCitation']['KeywordList'] != []:
    #     for kw in np.arange(1,np.size(paper['MedlineCitation']['KeywordList'][0])):
    #         print(paper['MedlineCitation']['KeywordList'][0][kw-1][:])
    # else:
    #     print("NO_KEYWORDS")
    print("<br>") #linebreak for github md 
    #end keywords test
    print("")
