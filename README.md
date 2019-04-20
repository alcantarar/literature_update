# Biomechanics Literature Update
#### Ryan Alcantara & Gary Bruening
We use [Machine Learning](Assets/ML.gif) to predict the general topic of a biomechanics-related paper given its title. To accomplish this, we:

1. Developed an HTML web scraper to extract the paper information and assigned paper topic from every [Biomch-L](https://biomch-l.isbweb.org/forums/7-Literature-Update) Literature Update since 2010. (`webscraper.py`)
2. Trained and compared multiple classification Machine Learning algorithms (`keras_1.py` & `test_many_ML_algorithms.ipynb`)
3. Created a python script (`literature_search.ipynb`) that: 
    1. Searches [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) for Biomechanics-related papers published in the past week,
    2. Uses the top-performing Machine Learning model (`keras-1`, a Covolutional Neural Network) to predict the paper topic for the week’s papers,
    3. Compiles papers, formats their citation, and organizes them by topic, saving to .md file here: [Literature Updates](/Literature_Updates).

### Packages
* [Bioython](https://biopython.org/wiki/Download) is used to access PubMed
* [Keras](https://keras.io/) and [Scikit-learn](https://scikit-learn.org/stable/) are used to construct ML models
