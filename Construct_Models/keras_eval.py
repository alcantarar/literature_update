# -*- coding: utf-8 -*-
"""
Runs the CNN created in keras_1.py on a data set.
Currently it's set to run on the 'text' variable, which is a list of strings.

Needs to load the model: model.json
    label encoder:       LabelEncoder.npy
    and vectorizer:      Vectorizer.pkl

@author: Gary
"""
##========================= Load the Model =====================================
from keras.models import model_from_json
# load json and create model
json_file = open('model_4_24.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model_4_24.h5")
model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
print("Loaded model from disk")

import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

vect = pickle.load(open('Vectorizer_tdif.pkl','rb'))
#le = LabelEncoder()
#le.classes_   = np.load('LabelEncoder.npy')
print('Loaded Vectorizer')

with open('unique_topics.txt', "rb") as fp:   # Unpickling
    unique_topic = pickle.load(fp)
print('Loaded Unique Topics')
 
#========================= Eval on test =======================================
import pickle
import numpy as np
import pandas as pd

text = ['neuromechanical effort, + = proxies estimation computational',
        'testing this other thing']

text = [text.lower() for text in text]
test = pd.DataFrame(data = {'title': text})
test = vect.transform(test['title'])
prediction_val = model.predict(test)

topics2 = [unique_topic[np.argmax(top_val)] for top_val in prediction_val]