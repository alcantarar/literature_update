# -*- coding: utf-8 -*-
"""
This script will fit a CNN to our webscrapped data saved in "RYANDATA_filt.csv'

The titles from the csv need to be converted into sparse matrices that reprsent
    the number of occurances of each word from the global bag of words present
    in each of the titles.
    
The topics from the csv need to be converted into a sparse matrix with number
     of columns equal to the number of unique topics.
     
Once fit it saves the model:      model.json
    Also saves the label encoder: LabelEncoder.npy
    and the vectorizer:           Vectorizer.pkl
    and the unique topics:        unique_topics.txt
=======
    
To test the model run keras_eval.py
    The testing data needs to be input as a list of strings, which is converted
    to a data frame, then the sparse matrix.

@author: Gary And Ryan
"""

import pandas as pd
import numpy as np
import string

#========================= Read in the Data ===================================

data = pd.read_csv('../Data/RYANDATA_filt.csv')
data = pd.read_csv('../Data/RYANDATA.csv')
print('Loading Data')   
unique_topics = list(data.Topics.unique())
topics = list(data.Topics)
titles = list(data.Titles)
authors = list(data.Authors)
journals = list(data.Journals)
years = list(data.Journals)
vol_isus = list(data.Vol_Isue)
dois = list(data.DOI)
abstracts = list(data.Abstract)
    
top = []
top_len = []
for k in np.arange(len(data['Topics'].unique())):
    top.append(data['Topics'].unique()[k])
    top_len.append(len(data[data['Topics']==top[k]]))

top_lengths = pd.DataFrame(data = {'Topics': top,
                                   'Length': top_len})
min_num = len(topics)
min_num = 1000
top_lengths = top_lengths.query('Length>=' + str(min_num))

filtered_data = pd.DataFrame(data =  {'Topics_split': [],
                                      'Topics': [],
                                      'Authors': [],
                                      'Titles': [],
                                      'Journals': [],
                                      'Years': [],
                                      'Vol_Isue': [],
                                      'DOI': [],
                                      'Abstract': []})

for top in top_lengths.Topics.unique():
    if not top == 'UNIQUETOPIC':
        filtered_data = filtered_data.append(data[data['Topics']==top],sort=True)

#breakhere
filtered_data_even = filtered_data.groupby('Topics').apply(lambda s: s.sample(1000))
filtered_data_even.fillna('')
data = filtered_data_even[['Topics_split','Topics','Authors','Titles','Journals','Years','Vol_Isue','DOI','Abstract']]

#data['abstracts']= ['']*len(data['Authors'])
#data.columns = ['num','topic_split','topic','authors','title','Journals','Years','Vol_Isue','DOI','abstract']
data.columns = ['topic_split','topic','authors','title','Journals','Years','Vol_Isue','DOI','abstract']

papers = pd.DataFrame(data['title'])
topic = pd.DataFrame(data['topic'])
author = pd.DataFrame(data['authors'])
abstract = pd.DataFrame(data['abstract'])
print("Number of Papers: " + str(len(papers)))
topic['topic'].unique()

# Make String Cleaner
def clean_str(abs_string,stop):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    abs_string = abs_string.translate(translator)
    abs_string = abs_string.split()
    abs_string = [word for word in abs_string if word not in stop]
    abs_string = ' '.join(abs_string)
    return abs_string
    
from nltk.corpus import stopwords
# Make the Stop Words
import string
stop = list(stopwords.words('english'))
stop_c = [string.capwords(word) for word in stop]
for word in stop_c:
    stop.append(word)
new_stop = ['StringElement','NlmCategory','Label','attributes','INTRODUCTION','METHODS','BACKGROUND','RESULTS','CONCLUSIONS']
for item in new_stop:
    stop.append(item)
    
papers['title'] = [clean_str(item,stop) for item in papers['title']]

#========================= Formatting Data ====================================
# Convert the data in the a sparse matrix.
# X is size Number of Articles by Number of Words in bag
# Y is size Number of Articles by Number of Unique Topics
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

feat = ['topic']
for x in feat:
    le = LabelEncoder()
    le.fit(list(topic[x].values))

np.save('../Models/Keras_model/LabelEncoder.npy',le.classes_)
print('Saved Label Encoder: LabelEncoder.npy')

data['everything'] = pd.DataFrame(papers['title'].astype(str)*4+data['abstract'].astype(str))
print(data['everything'].head(5))

def change(t):
    t = t.split()
    return ' '.join([(i) for (i) in t if i not in stop])

from nltk.corpus import stopwords
stop = list(stopwords.words('english'))
stop_c = [string.capwords(word) for word in stop]
for word in stop_c:
    stop.append(word)

data['everything'].apply(change)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

## Count Vectorizer
#vect = CountVectorizer()
#vect.fit(data['everything'])
#joblib.dump(vect,'../Models/Keras_model/Vectorizer_count.pkl')
#print('Saved Count Vectorizer: Vectorizer_count.pkl')
#vectors = vect.transform(data['everything'])
#
#vect2 = CountVectorizer()
#vect2.fit(topic)

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils.validation import check_is_fitted

try:
    vectorizer = vectorizer
    if check_is_fitted(vectorizer, '_tfidf'):
        vectorizer = TfidfVectorizer(min_df=20, #min occurances needed
                                     max_df=0.75, #max occuraces allowed (%)
                                     ngram_range=(1,2), #size range of grams (1-3 words)
                                     strip_accents='unicode',
                                     lowercase =True,
                                     analyzer='word', 
                                     token_pattern=r'\w+', 
                                     use_idf=True, 
                                     smooth_idf=True, 
                                     sublinear_tf=True, 
                                     stop_words = 'english')
except:
    vectorizer = TfidfVectorizer(min_df=20, #min occurances needed
                                 max_df=0.75, #max occuraces allowed (%)
                                 ngram_range=(1,2), #size range of grams (1-3 words)
                                 strip_accents='unicode',
                                 lowercase =True,
                                 analyzer='word', 
                                 token_pattern=r'\w+', 
                                 use_idf=True, 
                                 smooth_idf=True, 
                                 sublinear_tf=True, 
                                 stop_words = 'english')
    
vectors = vectorizer.fit_transform(data['everything'])
with open('../Models/Keras_model/Vectorizer_tdif.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
print('Saved Tdif Vectorizer: Vectorizer_tdif.pkl')

# Make the Sparse Topic Matrix
topic_dense = np.zeros(shape = [len(topic),len(topic.topic.unique())])
topic_unique = list(topic.topic.unique())
topic_unique_indx = []
for i, item in enumerate(topic.topic):
    topic_dense[i,topic_unique.index(item)] = 1
from scipy import sparse
topic_sparse = sparse.csr_matrix(topic_dense)
# Save the unique topics
with open('../Models/Keras_model/unique_topics.txt','wb') as fp:
    pickle.dump(topic_unique, fp)
    print('Saved Unique Topics: topic_unique.txt')

#========================= Split Into Test/Train ==============================
# Even Split
from sklearn.model_selection import StratifiedShuffleSplit
sss  = StratifiedShuffleSplit(n_splits = 1,train_size = 0.95, test_size=0.05,random_state=42)
sss.get_n_splits(vectors,topic_dense)

for train_index, test_index in sss.split(vectors, topic_dense):
    X_train, X_test = vectors[train_index], vectors[test_index]
    y_train, y_test = topic_dense[train_index], topic_dense[test_index]

y_train = sparse.csr_matrix(y_train)
y_test  = sparse.csr_matrix(y_test)

# Uneven Split
#X_train, X_test, y_train, y_test = train_test_split(vectors,
#                                                    topic_sparse,#topic['topic'],
#                                                    test_size=0.05,
#                                                    random_state = 0,
#                                                    stratify=topic_sparse)

print('X_Train shape: ' + str(X_train.shape))
input_dim = X_train.shape[1]  # Number of features
num_words = X_train.shape[1]
vocab_size = X_train.shape[1]
embedding_dim = 100

#========================= Build the Neural net ===============================
# Have 3 layers, first layer with 500 units, next two with 100 each.
# Output layer needs to have the same number of units as Num Topics

from keras.models import Sequential
from keras import layers
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding, Flatten
from keras import regularizers
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV

def create_model(first_layer, dropout_rate, n_2nd_layers):
#    first_layer = 1000
    activation = 'relu'
#    dropout_rate = 0.5
    
    model = Sequential()
#    model.add(layers.Conv1D(128, 5, activation='relu'))
#    model.add(Dropout(.2)),
    model.add(layers.Dense(first_layer, input_dim=input_dim, activation=activation))
    model.add(Dropout(dropout_rate))
    model.add(layers.Dense(200,activation = 'relu'))
#    for k in np.arange(n_2nd_layers):
#        model.add(layers.Dense(100,activation = 'relu'))
    model.add(layers.Dense(y_test.shape[1], activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', 
                  optimizer='adam', 
                  metrics=['accuracy'])
    return model

#========================= Trying Random Search ===============================
#from keras.wrappers.scikit_learn import KerasRegressor
#from sklearn.model_selection     import RandomizedSearchCV
#
#clf = KerasRegressor(build_fn=create_model, verbose=0)
#param_grid = dict(first_layer = [500,1000,1500], 
#                  dropout_rate = [.2,.5,.8], 
#                  n_2nd_layers = [0,1,2])
#
## Apply grid search
#grid = RandomizedSearchCV(clf, 
#                          param_distributions=param_grid,
#                          n_jobs=1, cv=3,
#                          verbose=2, n_iter=30)
#grid.fit(vectors,topic2)
#
## What were the best hyperparameters that we found?
#print(grid.best_params_)
#breakhere
    
#========================= Fit the Neural net =================================
# Set callback functions to early stop training and save the best model so far
from keras.callbacks import EarlyStopping, ModelCheckpoint
callbacks = [EarlyStopping(monitor='val_loss', patience=3),
             ModelCheckpoint(filepath='../Models/Keras_model/best_model.h5', monitor='vaL_acc', save_best_only=True)]

model = create_model(1000, .7, 0)
model.summary()
history = model.fit(X_train, y_train,
                    epochs=10,
                    callbacks = callbacks,
                    verbose=1,
                    validation_data=(X_test, y_test),
                    batch_size=1010)

import matplotlib.pyplot as plt
# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

#========================= Save the Model =====================================
from keras.models import model_from_json
import pickle
model.save('../Models/Keras_model/model_DNN.h5')
#model_json = model.to_json()
#with open("../Models/Keras_model/model_4_24.json", "w") as json_file:
#    json_file.write(model_json)
# serialize weights to HDF5
#model.save_weights("../Models/Keras_model/model_4_24.h5")
print("Saved model to disk: model_DNN.h5")
    
import os
if os.path.isfile('../Models/Keras_model/LabelEncoder.npy'):
    print('Saved Label Encoder: LabelEncoder.npy')
else:
    print('NO LABEL ENCODER SAVED')

if os.path.isfile('../Models/Keras_model/unique_topics.txt'):
    print('Saved Unique Topics: unique_topics.txt')
else:
    print('NO UNIQUE TOPICS SAVED')
    
if os.path.isfile('../Models/Keras_model/Vectorizer_tdif.pkl'):
    print('Saved Vectorizer: Vectorizer.pkl')
else:
    print('NO VECTORIZER SAVED')

#========================= Load the Model =====================================
from keras.models import model_from_json
from keras.models import load_model
model = load_model('../Models/Keras_model/best_model.h5')
model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
print("Loaded model from disk")

import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

vect = pickle.load(open('../Models/Keras_model/Vectorizer_tdif.pkl','rb'))
print('Loaded Vectorizer')

with open('../Models/Keras_model/unique_topics.txt', "rb") as fp: # Unpickling
    unique_topic = pickle.load(fp)
print('Loaded Unique Topics')

#========================= Plot Confusion Matrix ==============================
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

model_pred = model.predict(X_test)
topic_pred = [topic_unique[np.argmax(row)] for row in model_pred]
topic_act = [topic_unique[np.argmax(row)] for row in y_test]

conf_mat = confusion_matrix(topic_act, topic_pred)
print('Accuracy: ' + str(round(sum(np.diagonal(conf_mat))/X_test.shape[0]*100,1)) + '%')
accuracy = round(sum(np.diagonal(conf_mat))/X_test.shape[0]*100,1)
conf_mat_rowsum = [sum(row) for row in conf_mat]
conf_mat_perc = [row/sum(row) for row in conf_mat]
conf_mat_perc = np.stack(conf_mat_perc)

fig, ax = plt.subplots(figsize=(16,9))
sns.set(font_scale=1.2) #font size multiplier
sns.heatmap(conf_mat_perc, annot=True, fmt='.0%', cmap = 'magma', annot_kws={"size": 12},
            xticklabels=topic_unique, yticklabels=topic_unique)

plt.ylabel('Actual',fontsize = 20)
plt.xlabel('Predicted',fontsize = 20)
plt.yticks(size = 9)
plt.xticks(size = 9, rotation=30,ha='right')
title_str = 'Percent Predicted Correct, Global Accuracy: ' + str(accuracy) + '%'
plt.title(title_str, fontsize = 26)
plt.yticks( rotation='horizontal')
fig.tight_layout(pad = 2)
plt.savefig('../Plots/biomchL_predict_plot_DNN.png')

##========================= Find how many it missed ============================
##model_pred = model.predict(X_test)
#model_pred_alt = model_pred
#bad_topic = []
#topic_act2 = []
#topic_pred2 = []
#for i, row in enumerate(y_test):
##    if i % 100 == 0:
##        print('Testing Title: ' + str(i))
#    topic_act2.append(topic_unique[np.argmax(y_test[i,:])])
#    topic_pred2.append(topic_unique[np.argmax(model_pred_alt[i,:])])
#    if not topic_act2[i] == topic_pred2[i]:
##        bad_topic.append([topic_act2[i],topic_pred2[i]])
#        model_pred_alt[i,np.argmax(model_pred[i,:])] = 0
#        topic_pred2[i] = topic_unique[np.argmax(model_pred_alt[i,:])]
#        if not topic_act2[i] == topic_pred2[i]:
#            bad_topic.append([topic_act[i],topic_pred[i]])
            
##========================= Testing if vecotrizing worked ======================  
#unique_indx = [np.where(topic == item) for item in topic.topic.unique()]
#
#topic_unique = []
#topic_unique_indx = []
#for i, item in enumerate(topic.topic):
#    if item not in topic_unique:
#        topic_unique.append(item)
#        topic_unique_indx.append(i)
#    
#for i, item in enumerate(topic_unique_indx):
#    print(i,topic2[item,:])

##========================= Extra Layers  =====================================  
#model.add(layers.Embedding(vocab_size, embedding_dim, input_length=maxlen))
#model.add(layers.Conv1D(128, 5, activation='relu'))
#model.add(layers.GlobalMaxPooling1D())
#model.add(layers.LSTM(26, input_shape=(X_train.shape[0],X_train.shape[1]),return_sequences=True))
#model.add(Dropout(0.5))