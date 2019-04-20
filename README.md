We developed a Machine Learning algorithm to predict the general topic of a biomechanics-related paper given the title. To do this we had to:

1. Develop an HTML web scraper to extract the paper information and assigned paper topic from every [Biomch-L](https://biomch-l.isbweb.org/forums/7-Literature-Update) Literature Update since 2010. (`web scraper.py`)
2. Train and compare multiple classification Machine Learning algorithms (`keras_1.py` & `test_many_ML_algorithms.ipynb`)
3. Create a python script that searches [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) for Biomechanics-related papers published in the past week and uses the top-performing Machine Learning model to predict the paper topic for the week’s papers (`literature_search.ipynb`)
5. Compile papers, format and organize them by topic, saving to .md file (`literature_search.ipynb`).

# literature_update
Jupyter script performs pubmed search and prints citation where title hyperlinks to pubmed page via in markdown format. 

Dependencies: 
* biopython package (can be found [here](https://biopython.org/wiki/Download))
* numpy package (can be found [here](https://www.numpy.org/))

## Change search terms

Let's say you want to include fish biomechanics in your search. remove `NOT fish` from:

`search_results = search('(biomech*[Title/Abstract] OR locomot*[Title/Abstract]) AND bone*[Title/Abstract] NOT mice NOT fish NOT bird NOT rat NOT zoo')`

or completely change the `search()` parameters as you would for an [advanced pubmed search](https://www.ncbi.nlm.nih.gov/pubmed/advanced):

`search_results = search('(running) AND biomechanics')`

## Change date range of search

Change the numerical value for `reldate` :  
`reldate = 14, #only within two weeks from now`

