# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:24:56 2019

@author: Gary
"""


#========================= Load the Model =====================================
from keras.models import model_from_json
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
print("Loaded model from disk")
 
#========================= Eval on test =======================================
#score = loaded_model.evaluate(X_test, y_test, verbose=0)
#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

#text = 'neuromechanical effort proxies estimation computational'
#text = text.lower()

#test = pd.DataFrame(data = {'title': [text]})
#vectors = vectorizer.fit_transform(test['title'])
#vectors.shape

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
topics2 = [le.inverse_transform([np.argmax(top_val)])[0] for top_val in model.predict(test)]

#s = (vectorizer.transform(list(text)))
#print (s.shape)
#d = (loaded_model.predict(s))
#perc = np.exp(MNB.predict_log_proba(s)[0])
#le.inverse_transform(d)[0]
#print('Naive Bayes Accuracy: ' + '%.2f' % metrics.accuracy_score(y_test, MNB_pred) + '%')