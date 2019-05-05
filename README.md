# Biomechanics Literature Update
#### [Ryan Alcantara](https://twitter.com/Ryan_Alcantara_) & [Gary Bruening](https://twitter.com/garebearbru)

![Model_Accuracy](https://github.com/alcantarar/literature_update/blob/master/Plots/biomchL_predict_plot_DNN.png)

We use [Machine Learning](Assets/ML.gif) to predict the general topic of a biomechanics-related paper given its title. To accomplish this, we:

1. Developed an HTML [web scraper](Webscraper) to extract the paper information and assigned paper topic from every [Biomch-L](https://biomch-l.isbweb.org/forums/7-Literature-Update) Literature Update since 2010. (`webscraper.py`)
2. Trained and compared multiple classification Machine Learning algorithms ([`keras_1.py`](Construct_Models) & [`test_many_ML_algorithms_nn.ipynb`](Construct_Models))
3. Created a python script (`literature_search.ipynb`) that: 
    1. Searches [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) for Biomechanics-related papers published in the past week,
    2. Uses the top-performing Machine Learning model (`keras-1`, a Deep Neural Network with 73.5% accuracy) to predict the paper topic for the week’s papers,
    3. Compiles papers, formats their citation, and organizes them by topic, saving to .md file here: [Literature Updates](/Literature_Updates).

## Files
#### Assets  
A neato gif.
#### Construct_Models  
Contains the files to contstruct the models. Two main files `keras_1.py` and `test_many_ML_algorithms_nn.ipynb`.  
1. `keras_1.py` - Fits a deep neural network to data contained in [Data](Data). Saves the models into [models](Models/Keras_model). The vectorizer and label encoders are saved here as well.
2. `test_many_ML_algorithms_nn.ipynb` - Fits multiple machine learning methods to the [Data](Data). Includes [Multinomial Naive Payes](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html), [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [Stochastic Gradient Descent (SGD)](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html), [Linear Support Vector Classification](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html)), and [Multi-layer Perceptron Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html). Saves the data into [models](Models/Many_ML_models). The vectorizer and label encoders are saved here as well.
3. `keras_eval.py` - A small script to evaluate the keras neural network on test strings.
#### Data  
Where the webscraped data is stored.  
1. [RYANDATA.csv](Data/RYANDATA.csv) - The full csv file including paper number, Category/Topic, Authors, Title, Journal, Year, Volume and Issue, DOI, and Abstract. Named this way because Gary just thought he would hand the data off and not get really really caught up in this. Boy, was he wrong.
2. [RYANDATA_filt.csv](RYANDATA_filt.csv) - Has all the same headers as RYANDATA.csv, but filters out topics that represent less than 5% of the total papers.
3. [RYANDATA_filt_even.csv](RYANDATA_filt_even.csv) - An evenly downsampled (by topic) csv of RYANDATA_filt.csv. Each topic has the same number of representations in this csv.
#### Literature_Updates  
Where weekly updates can be stored in markdown & csv format for publishing.  
#### Models  
Where all the model files are saved after being created.  
1. Keras_model - Location of all the Keras Neural Net files. Some neural net files are to large to upload to Git on their own so are split. Using [7-zip](https://www.howtogeek.com/howto/36947/how-to-upload-really-large-files-to-skydrive-dropbox-or-email/)(Windows) or [Keka](https://github.com/aonez/Keka) (MacOS) you can recombine these files to create the model file and weights file.
2. Many_ML_models - Location of all the many ML testing files are saved. The mpl file will need to be recombined using 7-zip/Keka similar to the Keras Neural Net files.
#### Plots  
Model validation plots are saved here. Usually a confusion matrix.  
#### Webscraper  
The python file to scrape the [Biomch-L](https://biomch-l.isbweb.org/forums/7-Literature-Update) forum.  
#### `literature_search.ipynb`  
Ipython Notebook to generate the literature update. Uses Biopython `v1.73` to perfrom a literature search, then the a given ML model to classify the papers. Saves the results in a markdown file in [literature update](Literature_Updates).  
### Unique Packages
* [BeautifySoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is used to scrape the web for the articles to feed into the ML models.
* [Keras](https://keras.io/) and [Scikit-learn](https://scikit-learn.org/stable/) are used to construct ML models.
* [Biopython](https://biopython.org/wiki/Download) is used to access PubMed. Requires version `1.73` or newer.
