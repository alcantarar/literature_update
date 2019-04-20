# Biomechanics Literature Update
#### Ryan Alcantara & Gary Bruening
We developed use [Machine Learning](ML.gif) to predict the general topic of a biomechanics-related paper given its title. To accomplish this, we:

1. Developed an HTML web scraper to extract the paper information and assigned paper topic from every [Biomch-L](https://biomch-l.isbweb.org/forums/7-Literature-Update) Literature Update since 2010. (`webscraper.py`)
2. Trained and compared multiple classification Machine Learning algorithms (`keras_1.py` & `test_many_ML_algorithms.ipynb`)
3. Created a python script that 
    1. Searches [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) for Biomechanics-related papers published in the past week,
    2. Uses the top-performing Machine Learning model (`keras-1`) to predict the paper topic for the week’s papers (`literature_search.ipynb`),
    3. Compiles papers, formats their citation, and organizes them by topic, saving to .md file: `YYYY_MM_DD_lit_update.md`.

### Packages
* [bioython](https://biopython.org/wiki/Download) is used to access PubMed
* [keras](https://keras.io/) and [scikit-learn](https://scikit-learn.org/stable/) are used to construct ML models
