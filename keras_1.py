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
from sklearn.preprocessing import OneHotEncoder
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

#from sklearn.feature_extraction.text import TfidfVectorizer
#vectorizer = TfidfVectorizer(min_df=1, max_features=70000, strip_accents='unicode',lowercase =True,
#                            analyzer='word', token_pattern=r'\w+', use_idf=True, 
#                            smooth_idf=True, sublinear_tf=True, stop_words = 'english')
#vectors = vectorizer.fit_transform(data['everything'])
#vectors.shape

vect = CountVectorizer()
vect.fit(data['everything'])
joblib.dump(vect,'Vectorizer.pkl')
print('Saved Vectorizer: Vectorizer.pkl')

vectors = vect.transform(data['everything'])

encoder = OneHotEncoder(sparse = True)
topic = encoder.fit_transform(topic)

X_train, X_test, y_train, y_test = train_test_split(vectors,
                                                    topic,#topic['topic'],
                                                    test_size=0.1,
                                                    random_state = 0)

input_dim = X_train.shape[1]  # Number of features
num_words = X_train.shape[1]

#========================= Fit the Neural net =================================
# Have 3 layers, first layer with 500 units, next two with 100 each.
# Output layer needs to have the same number of units as Num Topics
from keras.models import Sequential
from keras import layers
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding

model = Sequential()
model.add(layers.Dense(500, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(100, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(100, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(27, activation='sigmoid'))

model.compile(loss='binary_crossentropy', 
    optimizer='adam', 
    metrics=['accuracy'])
model.summary()

history = model.fit(X_train, y_train,
                    epochs=500,
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
#from keras.models import model_from_json
#model_json = model.to_json()
#with open("model.json", "w") as json_file:
#    json_file.write(model_json)
## serialize weights to HDF5
#model.save_weights("model.h5")
#print("Saved model to disk: model.h5")
#import os
#if os.path.isfile('LabelEncoder.npy'):
#    print('Saved Label Encoder: LabelEncoder.npy')
#else:
#    print('NO LABEL ENCODER SAVED')
#    
#if os.path.isfile('LabelEncoder.npy'):
#    print('Saved Vectorizer: Vectorizer.pkl')
#else:
#    print('NO VECTORIZER SAVED')

from sklearn.metrics import confusion_matrix
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

vect = pickle.load(open('Vectorizer.pkl','rb'))
le = LabelEncoder()
le.classes_   = np.load('LabelEncoder.npy')
print('Loaded Vectorizer')

text = ['neuromechanical effort, + = proxies estimation computational',
        'testing this other thing']

text = [text.lower() for text in text]
test = pd.DataFrame(data = {'title': text})
test = vect.transform(test['title'])
prediction_val = model.predict(test)
topics2 = [le.inverse_transform([np.argmax(top_val)])[0] for top_val in model.predict(X_test)]
y_test_array = [le.inverse_transform([np.argmax(top_val)])[0] for top_val in y_test]

import seaborn as sns
import matplotlib.pyplot as plt
data['topic_id'] = data['topic'].factorize()[0]
topic_id_df = data[['topic',
                  'topic_id']].drop_duplicates().sort_values('topic_id')
topic_to_id = dict(topic_id_df.values)
id_to_topic = dict(topic_id_df[['topic_id','topic']].values)
data.sample(5)

conf_mat = confusion_matrix(y_test_array, topics2)
conf_mat_rowsum = [sum(row) for row in conf_mat]
conf_mat_perc = [row/sum(row) for row in conf_mat]
conf_mat_perc = np.stack(conf_mat_perc = [row/sum(row) for row in conf_mat])

fig, ax = plt.subplots(figsize=(10,10))
sns.set(font_scale=1.2) #font size multiplier
sns.heatmap(conf_mat_perc, annot=True, fmt='.3f', cmap = 'magma', annot_kws={"size": 8},
            xticklabels=topic_id_df.topic.values, yticklabels=topic_id_df.topic.values)

plt.ylabel('Actual',fontsize = 20)
plt.xlabel('Predicted',fontsize = 20)
plt.yticks(size = 7)
plt.xticks(size = 7, rotation=30,ha='right')
plt.title('Percent Predicted Correct', fontsize = 26)
plt.yticks( rotation='horizontal')
fig.tight_layout(pad = 2)

plt.savefig('biomchL_predict_plot.png')

    
















