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
<<<<<<< HEAD
    and the unique topics:        unique_topics.txt
=======
>>>>>>> master
    
To test the model run keras_eval.py
    The testing data needs to be input as a list of strings, which is converted
    to a data frame, then the sparse matrix.

@author: Gary
"""

import pandas as pd
import numpy as np
import string

#========================= Read in the Data ===================================

data = pd.read_csv('../Data/RYANDATA_filt.csv')
data.columns = ['num','topic_split','topic','authors','title','Journals','Years','Vol_Isue','DOI','abstract']

papers = pd.DataFrame(data['title'])
topic = pd.DataFrame(data['topic'])
author = pd.DataFrame(data['authors'])
abstract = pd.DataFrame(data['abstract'])
print("Number of Papers: " + str(len(papers)))
topic['topic'].unique()

# Make String Cleaner
def clean_str(abs_string,stop):
#    print(abs_string)
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

<<<<<<< HEAD
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

vect = CountVectorizer()
vect.fit(data['everything'])
joblib.dump(vect,'../Models/Keras_model/Vectorizer_count.pkl')
print('Saved Count Vectorizer: Vectorizer_count.pkl')
vectors = vect.transform(data['everything'])

vect2 = CountVectorizer()
vect2.fit(topic)

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
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
topic_sparse = np.zeros(shape = [len(topic),len(topic.topic.unique())])
topic_unique = list(topic.topic.unique())
topic_unique_indx = []
for i, item in enumerate(topic.topic):
    topic_sparse[i,topic_unique.index(item)] = 1
from scipy import sparse
topic2 = sparse.csr_matrix(topic_sparse)
# Save the unique topics
with open('../Models/Keras_model/unique_topics.txt','wb') as fp:
    pickle.dump(topic_unique, fp)
    print('Saved Unique Topics: topic_unique.txt')

X_train, X_test, y_train, y_test = train_test_split(vectors,
                                                    topic2,#topic['topic'],
                                                    test_size=0.2,
                                                    random_state = 0)

input_dim = X_train.shape[1]  # Number of features
num_words = X_train.shape[1]
vocab_size = X_train.shape[1]
embedding_dim = 100

##========================= Fit the Neural net =================================
## Have 3 layers, first layer with 500 units, next two with 100 each.
## Output layer needs to have the same number of units as Num Topics
#
#from keras.models import Sequential
#from keras import layers
#from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
#from keras import regularizers
#
#model = Sequential()
#model.add(layers.Dense(3000, input_dim=input_dim, activation='relu'))
#model.add(Dropout(0.5))
#model.add(layers.Dense(500, input_dim=input_dim, activation='relu'))
#model.add(Dropout(0.5))
#model.add(layers.Dense(y_test.shape[1], activation='sigmoid'))
#
#model.compile(loss='binary_crossentropy', 
#    optimizer='adam', 
#    metrics=['accuracy'])
#model.summary()
#
## Set callback functions to early stop training and save the best model so far
#from keras.callbacks import EarlyStopping, ModelCheckpoint
#callbacks = [EarlyStopping(monitor='val_loss', patience=2),
#             ModelCheckpoint(filepath='../Models/Keras_model/best_model.h5', monitor='val_loss', save_best_only=True)]
#
#history = model.fit(X_train, y_train,
#                    epochs=50,
#                    callbacks = callbacks,
#                    verbose=2,
#                    validation_data=(X_test, y_test),
#                    batch_size=500)
#
##loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
##print("Training Accuracy: {:.4f}".format(accuracy))
##loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
##print("Testing Accuracy:  {:.4f}".format(accuracy))
#
#import matplotlib.pyplot as plt
## Plot training & validation accuracy values
##plt.plot(history.history['acc'])
##plt.plot(history.history['val_acc'])
##plt.title('Model accuracy')
##plt.ylabel('Accuracy')
##plt.xlabel('Epoch')
##plt.legend(['Train', 'Test'], loc='upper left')
##plt.show()

#========================= Save the Model =====================================
#from keras.models import model_from_json
#import pickle
#model_json = model.to_json()
#with open("../Models/Keras_model/model_4_24.json", "w") as json_file:
#    json_file.write(model_json)
## serialize weights to HDF5
#model.save_weights("../Models/Keras_model/model_4_24.h5")
#print("Saved model to disk: model.json")
    
import os
if os.path.isfile('../Models/Keras_model/LabelEncoder.npy'):
    print('Saved Label Encoder: LabelEncoder.npy')
else:
    print('NO LABEL ENCODER SAVED')

if os.path.isfile('../Models/Keras_model/unique_topics.txt'):
    print('Saved Unique Topics: unique_topics.txt')
else:
    print('NO UNIQUE TOPICS SAVED')
    
if os.path.isfile('../Models/Keras_model/LabelEncoder.npy'):
    print('Saved Vectorizer: Vectorizer.pkl')
else:
    print('NO VECTORIZER SAVED')

#========================= Load the Model =====================================
from keras.models import model_from_json
# load json and create model
json_file = open('../Models/Keras_model/model_4_24.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
#model.load_weights("model_4_24.h5")
model.load_weights("../Models/Keras_model/best_model.h5")
model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
print("Loaded model from disk")

import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

vect = pickle.load(open('../Models/Keras_model/Vectorizer_tdif.pkl','rb'))
#le = LabelEncoder()
#le.classes_   = np.load('LabelEncoder.npy')
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
