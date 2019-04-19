# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:20:04 2019

@author: Gary
"""

import numpy as np
import pandas as pd
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv('RYANDATA_filt.csv')
data.columns = ['num','topic','authors','title','Journals','Years','Vol_Isue','DOI']

columns = data.columns
# print(columns)


papers = pd.DataFrame(data['title'])
topic = pd.DataFrame(data['topic'])
author = pd.DataFrame(data['authors'])

print("Number of Papers: " + str(len(papers)))
#print(len(topic))
# topic.head(2)
# papers[0:100]

topic['topic'].unique()

from sklearn.preprocessing import LabelEncoder

feat = ['topic']
for x in feat:
    le = LabelEncoder()
    le.fit(list(topic[x].values))
    topic[x] = le.transform(list(topic[x]))
    
topic['topic'].unique()

le.inverse_transform([0])[0]

data['everything'] = pd.DataFrame(data['title'] + ' ' + data['authors'])
print(data['everything'].head(5))

def change(t):
    t = t.split()
    return ' '.join([(i) for (i) in t if i not in stop])

#import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
stop = list(stopwords.words('english'))
stop_c = [string.capwords(word) for word in stop]
for word in stop_c:
    stop.append(word)

data['everything'].apply(change)

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(min_df=2, max_features=70000, strip_accents='unicode',lowercase =True,
                            analyzer='word', token_pattern=r'\w+', use_idf=True, 
                            smooth_idf=True, sublinear_tf=True, stop_words = 'english')
vectors = vectorizer.fit_transform(data['everything'])
vectors.shape

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

X_train, X_test, y_train, y_test = train_test_split(vectors,
                                                    topic['topic'],
                                                    test_size=0.3,
                                                    random_state = 0)

print (X_train.shape)
print (y_train.shape)
print (X_test.shape)
print (y_test.shape)

type(papers)

# Multinomial Naive Bayes
MNB = MultinomialNB(alpha=.45)
MNB.fit(X_train, y_train)
MNB_pred = MNB.predict(X_test)
#print (metrics.f1_score(y_test, MNB_pred, average='macro'))

text = 'neuromechanical effort proxies estimation computational'
text = text.lower()
s = (vectorizer.transform(list(text)))
print (s.shape)
d = (MNB.predict(s))
perc = np.exp(MNB.predict_log_proba(s)[0])
le.inverse_transform(d)[0]
print('Naive Bayes Accuracy: ' + '%.2f' % metrics.accuracy_score(y_test, MNB_pred) + '%')

from sklearn.externals import joblib
joblib.dump(MNB, 'MultinomialNB.pkl')
#print ("Model Saved")

# Logistic Regression
from sklearn import linear_model
LogR = linear_model.LogisticRegression(solver= 'sag',max_iter=200,random_state=450, multi_class='multinomial')
LogR.fit(X_train, y_train)
LogR_pred = LogR.predict(X_test)
#print (metrics.f1_score(y_test, LogR_pred, average='macro'))
print('Logistic Regression: ' + '%.2f' % metrics.accuracy_score(y_test, LogR_pred) + '%')

# Stochastic Gradient Descent (SGD) learning
from sklearn.linear_model import SGDClassifier
sgd = SGDClassifier(max_iter=500, random_state=0, tol = 1e-3)
sgd.fit(X_train, y_train) 
sgd_pred = sgd.predict(X_test)
#print (metrics.f1_score(y_test, sgd_pred, average='macro'))
#print (metrics.accuracy_score(y_test, sgd_pred))
print('Stochastic Gradient: ' + '%.2f' % metrics.accuracy_score(y_test, sgd_pred) + '%')

# Linear SVC
from sklearn.svm import LinearSVC
lsvc = LinearSVC()
lsvc.fit(X_train, y_train) 
lsvc_pred = lsvc.predict(X_test)
#print (metrics.f1_score(y_test, lsvc_pred, average='macro'))
#print (metrics.accuracy_score(y_test, lsvc_pred))
print('Linear SVC: ' + '%.2f' % metrics.accuracy_score(y_test, lsvc_pred) + '%')

## Neural Net
#from sklearn.neural_network import MLPClassifier
#clf = MLPClassifier(activation='logistic', alpha=0.00003, batch_size='auto',
#                   beta_1=0.9, beta_2=0.999, early_stopping=False,
#                   epsilon=1e-08, hidden_layer_sizes=(20,), learning_rate='constant',
#                   learning_rate_init=0.003, max_iter=200, momentum=0.9,
#                   nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
#                   solver='adam', tol=0.0001, validation_fraction=0.1, verbose=False,
#                   warm_start=False)
#clf.fit(X_train, y_train) 
#pred = clf.predict(X_test)
#print (metrics.f1_score(y_test, pred, average='macro'))
#print (metrics.accuracy_score(y_test, pred))
#
#text = ['Calcaneus range of motion underestimated by markers on running shoe heel']
##text = list(text)
#s = (vectorizer.transform(text))
##s = vectorizer.fit_transform(df)
#print (s.shape)
#d = (clf.predict(s))
#le.inverse_transform(d)[0]























