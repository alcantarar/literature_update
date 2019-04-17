#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:45:46 2019

@author: ryanalcantara
"""


import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer

#mac
#df = pd.read_csv("/Users/ryanalcantara/Google Drive/Subreddit/biomch_l_list.csv")
#pc
df = pd.read_csv("RYANDATA_filt.csv")
df.columns = ['Num','topic','Authors','title','Journals','Years','Vol_Isue','DOI']
df = df[df.Num % 4 ==1]
df = df[df.topic != 'UNIQUETOPIC']

col = ['topic','title']
df = df[col]
df = df[pd.notnull(df['title'])]

df.columns = ['topic','title']

df['topic_id'] = df['topic'].factorize()[0]
topic_id_df = df[['topic',
                  'topic_id']].drop_duplicates().sort_values('topic_id')
topic_to_id = dict(topic_id_df.values)
id_to_topic = dict(topic_id_df[['topic_id','topic']].values)
df.sample(5)

#histo of topics (ideally have >600 each)
#plt.rc('xtick',labelsize = 12)
#plt.rc('ytick',labelsize = 12)
#fig = plt.figure(figsize= (10,5))
#df.groupby('topic').title.count().plot.bar(ylim=0)
#plt.xlabel("paper topic",fontsize = 12)
#plt.show()


# %% test linear svc
tfidf = TfidfVectorizer(sublinear_tf = True,
                       min_df = 1,
                       norm = 'l2',
                       encoding = 'latin-1',
                       ngram_range = (1,2),
                       stop_words = 'english')
# https://scikit-learn.org/stable/modules/multiclass.html
features = tfidf.fit_transform(df.title).toarray()
labels = df.topic_id

models = [
    #RandomForestClassifier(n_estimators=100, max_depth=3, random_state=0), #sucks
    LinearSVC(multi_class='ovr', random_state=0), #one vs rest (all)
#     SGDClassifier(max_iter=500, random_state=0, tol = 1e-3),
#     PassiveAggressiveClassifier(max_iter = 500, random_state = 0, tol = 1e-3)
    #MultinomialNB(),
    #LogisticRegression(random_state=0, solver = 'liblinear', multi_class = 'ovr'),
]
CV = 2
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
    model_name = model.__class__.__name__
    accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
    for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name, fold_idx, accuracy))

cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

# %%
import seaborn as sns
plt.rc('xtick',labelsize = 12)
plt.rc('ytick',labelsize = 12)
sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df, 
              size=8, jitter=True, edgecolor="gray", linewidth=2)

plt.xticks( rotation='25')

#plt.show()

cv_df.groupby('model_name').accuracy.mean()

# %%
model = LinearSVC()

X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
from sklearn.metrics import confusion_matrix
plt.rc('xtick',labelsize = 6)
plt.rc('ytick',labelsize = 6)
conf_mat = confusion_matrix(y_test, y_pred)
conf_mat_rowsum = [sum(row) for row in conf_mat]
conf_mat_perc = conf_mat / conf_mat_rowsum
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
