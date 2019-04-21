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
    
To test the model run keras_eval.py
    The testing data needs to be input as a list of strings, which is converted
    to a data frame, then the sparse matrix.

@author: Gary
"""

import pandas as pd
import numpy as np
import string

#========================= Read in the Data ===================================
data = pd.read_csv('RYANDATA_filt.csv')
data.columns = ['num','topic','authors','title','Journals','Years','Vol_Isue','DOI']

papers = pd.DataFrame(data['title'])
topic = pd.DataFrame(data['topic'])
author = pd.DataFrame(data['authors'])
print("Number of Papers: " + str(len(papers)))
topic['topic'].unique()

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

np.save('LabelEncoder.npy',le.classes_)
print('Saved Label Encoder: LabelEncoder.npy')

data['everything'] = pd.DataFrame(data['title'])
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
joblib.dump(vect,'Vectorizer.pkl')
print('Saved Vectorizer: Vectorizer.pkl')
vectors = vect.transform(data['everything'])

vect2 = CountVectorizer()
vect2.fit(topic)

topic_sparse = np.zeros(shape = [len(topic),len(topic.topic.unique())])
topic_unique = list(topic.topic.unique())
topic_unique_indx = []
for i, item in enumerate(topic.topic):
    topic_sparse[i,topic_unique.index(item)] = 1
from scipy import sparse
topic2 = sparse.csr_matrix(topic_sparse)
# Save the unique topics
with open('unique_topics.txt','wb') as fp:
    pickle.dump(topic_unique, fp)

X_train, X_test, y_train, y_test = train_test_split(vectors,
                                                    topic2,#topic['topic'],
                                                    test_size=0.2,
                                                    random_state = 0)

input_dim = X_train.shape[1]  # Number of features
num_words = X_train.shape[1]

#========================= Fit the Neural net =================================
# Have 3 layers, first layer with 500 units, next two with 100 each.
# Output layer needs to have the same number of units as Num Topics

from keras.models import Sequential
from keras import layers
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
from keras import regularizers

model = Sequential()
model.add(layers.Dense(100, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(50, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(26, activation='sigmoid'))

model.compile(loss='binary_crossentropy', 
    optimizer='adam', 
    metrics=['accuracy'])
model.summary()

history = model.fit(X_train, y_train,
                    epochs=500,
                    verbose=2,
                    validation_data=(X_test, y_test),
                    batch_size=500)

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
import pickle
model_json = model.to_json()
with open("model_4_21.json", "w") as json_file:
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

##========================= Load the Model =====================================
#from keras.models import model_from_json
## load json and create model
#json_file = open('model.json', 'r')
#loaded_model_json = json_file.read()
#json_file.close()
#model = model_from_json(loaded_model_json)
## load weights into new model
#model.load_weights("model.h5")
#model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
#print("Loaded model from disk")
#
#import pickle
#import numpy as np
#import pandas as pd
#from sklearn.preprocessing import LabelEncoder
#
#vect = pickle.load(open('Vectorizer.pkl','rb'))
#le = LabelEncoder()
#le.classes_   = np.load('LabelEncoder.npy')
#print('Loaded Vectorizer')
#
#text = ['neuromechanical effort, + = proxies estimation computational',
#        'testing this other thing']
#
#text = [text.lower() for text in text]
#test = pd.DataFrame(data = {'title': text})
#test = vect.transform(test['title'])
#prediction_val = model.predict(test)

#========================= Plot Confusion Matrix ==============================
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

model_pred = model.predict(X_test)
topics2 = [topic_unique[np.argmax(top_val)] for top_val in model_pred]
y_test_array = [topic_unique[np.argmax(top_val)] for top_val in y_test]

conf_mat = confusion_matrix(y_test_array, topics2)
conf_mat_rowsum = [sum(row) for row in conf_mat]
conf_mat_perc = [row/sum(row) for row in conf_mat]
conf_mat_perc = np.stack(conf_mat_perc)

fig, ax = plt.subplots(figsize=(10,10))
sns.set(font_scale=1.2) #font size multiplier
sns.heatmap(conf_mat_perc, annot=True, fmt='.3f', cmap = 'magma', annot_kws={"size": 8},
            xticklabels=topic_unique, yticklabels=topic_unique)

plt.ylabel('Actual',fontsize = 20)
plt.xlabel('Predicted',fontsize = 20)
plt.yticks(size = 7)
plt.xticks(size = 7, rotation=30,ha='right')
plt.title('Percent Predicted Correct', fontsize = 26)
plt.yticks( rotation='horizontal')
fig.tight_layout(pad = 2)
plt.savefig('biomchL_predict_plot.png')

bad_topic = []
for i, row in enumerate(y_test):
    model_pred = model.predict(X_test[i,:])
    topic_act = topic_unique[np.argmax(y_test[i,:])]
    topic_pred = topic_unique[np.argmax(model_pred)]
    if not topic_act == topic_pred:
        model_pred[0][np.argmax(model_pred)] = 0
        topic_pred = topic_unique[np.argmax(model_pred)]
        if not topic_act == topic_pred:
            bad_topic.append([topic_act,topic_pred])
            break
  
#========================= Testing if vecotrizing worked ======================  
unique_indx = [np.where(topic == item) for item in topic.topic.unique()]

topic_unique = []
topic_unique_indx = []
for i, item in enumerate(topic.topic):
    if item not in topic_unique:
        topic_unique.append(item)
        topic_unique_indx.append(i)
    
for i, item in enumerate(topic_unique_indx):
    print(i,topic2[item,:])















