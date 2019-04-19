# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:20:59 2019

@author: Gary
"""

import pandas as pd
import numpy as np
import string

data = pd.read_csv('RYANDATA_filt.csv')
data.columns = ['num','topic','authors','title','Journals','Years','Vol_Isue','DOI']

papers = pd.DataFrame(data['title'])
topic = pd.DataFrame(data['topic'])
author = pd.DataFrame(data['authors'])

print("Number of Papers: " + str(len(papers)))

topic['topic'].unique()

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.externals import joblib

feat = ['topic']
for x in feat:
    le = LabelEncoder()
    le.fit(list(topic[x].values))
#    topic[x] = le.transform(list(topic[x]))

np.save('LabelEncoder.npy',le.classes_)
print('Saved Label Encoder: LabelEncoder.npy')

data['everything'] = pd.DataFrame(data['title'])# + ' ' + data['authors'])
print(data['everything'].head(5))
#data = data.sample(n=30)
#topic = topic.sample(n=30)

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
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import Tokenizer

vectorizer = TfidfVectorizer(min_df=1, max_features=70000, strip_accents='unicode',lowercase =True,
                            analyzer='word', token_pattern=r'\w+', use_idf=True, 
                            smooth_idf=True, sublinear_tf=True, stop_words = 'english')
vectors = vectorizer.fit_transform(data['everything'])
vectors.shape

vect = CountVectorizer()
vect.fit(data['everything'])
from sklearn.externals import joblib
joblib.dump(vect,'Vectorizer.pkl')
print('Saved Vectorizer: Vectorizer.pkl')

vectors = vect.transform(data['everything'])

encoder = OneHotEncoder(sparse = True)
topic = encoder.fit_transform(topic)

#vectors = vectorizer.fit_transform(test['title'])
#vectors.shape

#tokenizer = Tokenizer(num_words=70000)
#tokenizer.fit_on_texts(data['everything'])
#vectors = tokenizer.texts_to_sequences(data['everything'])
#tokenizer.texts_to_sequences(test['title'])
# NEED TO CONVERT THE VECTORS TO SPARSE MATRIX

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from keras.utils import np_utils

X_train, X_test, y_train, y_test = train_test_split(vectors,
                                                    topic,#topic['topic'],
                                                    test_size=0.1,
                                                    random_state = 0)

input_dim = X_train.shape[1]  # Number of features
num_words = X_train.shape[1]
#y_train = np_utils.to_categorical(y_train, 27)
#y_test = np_utils.to_categorical(y_test, 27)

from keras.models import Sequential
from keras import layers
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding

model = Sequential()
#model.add(LSTM(64, input_shape = X_test.shape, return_sequences=True, 
#               dropout=0.1, recurrent_dropout=0.1))
model.add(layers.Dense(500, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(100, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(100, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(27, activation='sigmoid'))

## Recurrent layer
#model = Sequential()
#model.add(LSTM(64, return_sequences=False, 
#               dropout=0.1, recurrent_dropout=0.1))
#
## Fully connected layer
#model.add(Dense(64, activation='relu'))
#
## Dropout for regularization
#model.add(Dropout(0.5))
#
## Output layer
#model.add(Dense(num_words, activation='softmax'))
#
## Compile the model
#model.compile(
#    optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#
model.compile(loss='binary_crossentropy', 
    optimizer='adam', 
    metrics=['accuracy'])
model.summary()

# Batch size is how many samples to train on
# For 1000 samples, then batch=100 means 10 trainings per epoch
history = model.fit(X_train, y_train,
                    epochs=100,
                    verbose=2,
                    validation_data=(X_test, y_test),
                    batch_size=3000)

loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))

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
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk: model.h5")
import os
if os.path.isfile('LabelEncoder.npy'):
    print('Saved Label Encoder: LabelEncoder.npy')
else:
    print('NO LABEL ENCODER SAVED')
    
if os.path.isfile('LabelEncoder.npy'):
    print('Saved Vectorizer: Vectorizer.pkl')
else:
    print('NO VECTORIZER SAVED')
    
















