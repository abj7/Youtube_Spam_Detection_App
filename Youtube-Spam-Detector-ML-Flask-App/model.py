import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from pprint import pprint

import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Data Processing
df1 = pd.read_csv("data/Youtube01-Psy.csv")
df2 = pd.read_csv("data/Youtube02-KatyPerry.csv")
df3 = pd.read_csv("data/Youtube03-LMFAO.csv")
df4 = pd.read_csv("data/Youtube04-Eminem.csv")
df5 = pd.read_csv("data/Youtube05-Shakira.csv")
frames = [df1, df2, df3, df4, df5]
df = pd.concat(frames, keys = ["Psy", "KatyPerry", "LMFAO", "Eminem", "Shakira"])
df.to_csv("YoutubeSpamCombinedDataset.csv")

# Data is mostly cleaned already
df_x = df['CONTENT']
df_y = df['CLASS']

# 2 different comment text vectorizations
corpus = df_x
cv = CountVectorizer()
X = cv.fit_transform(corpus)

tv = TfidfVectorizer()
X2 = tv.fit_transform(corpus)

# Model Fitting (Naive Bayes w/ CountVectorizer)
X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.3, random_state=7)
clf = MultinomialNB()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
conf_mat = confusion_matrix(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("Accuracy of Naive Bayes Model using CountVec = ", clf.score(X_test, y_test))
print(conf_mat)
print(f1)

# Model Fitting (Multinomial Naive Bayes w/ TfidfVectorizer)
# Multinomial Naive Bayes simply assumes multinomial distribution for data, which seem to be a
# reasonable assumption in the case of word counts in text.
X_train, X_test, y_train, y_test = train_test_split(X2, df_y, test_size=0.3, random_state=7)
clf2 = MultinomialNB()
clf2.fit(X_train, y_train)
y_pred = clf2.predict(X_test)
conf_mat = confusion_matrix(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("Accuracy of Naive Bayes Model using TfidfVec = ", clf2.score(X_test, y_test)*100, "%")
print(conf_mat)
print(f1)

# Model Tuning with GridSearch and Pipeline
#pipeline = Pipeline([('vec', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
#parameters = {
#    'vec__max_df': (0.5, 0.625, 0.75, 0.875, 1.0),
#    'vec__max_features': (None, 5000, 10000, 20000),
#    'vec__min_df': (1, 5, 10, 20, 50),
#    'tfidf__use_idf': (True, False),
#    'tfidf__sublinear_tf': (True, False),
#    'vec__binary': (True, False),
#    'tfidf__norm': ('l1', 'l2'),
#    'clf__alpha': (1, 0.1, 0.01, 0.001, 0.0001, 0.00001),
#    }

#grid_search = GridSearchCV(pipeline, parameters, scoring="accuracy", cv = 3)
#grid_search.fit(df_x, df_y)
#print('Best score:', grid_search.best_score_)
#print('Best parameters:', grid_search.best_params_)

def isSpam(x):
    if x == 1:
        return "Spam"
    else:
        return "Not Spam"

# example predictions 1 & 2
comment = ["Check out my youtube channel"]
vect = cv.transform(comment).toarray()
print(comment, " is ", isSpam(clf.predict(vect)), ".")
comment2 = ["THIS SONG IS AMAZING. I LOVE HER SO MUCH."]
vect2 = cv.transform(comment2).toarray()
print(comment2, " is ", isSpam(clf.predict(vect2)), ".")


# saving model
naivebayesML = open("YtbSpam_model.pkl","wb")
pickle.dump((clf, cv), naivebayesML)
naivebayesML.close()

# example prediction 3 using packaged model
ytb_model = open("YtbSpam_model.pkl","rb")
new_model = pickle.load(ytb_model)
comment3 = ["Definitely my favorite music video by this artist."]
vect3 = cv.transform(comment3).toarray()
print(comment3, " is ", isSpam(clf.predict(vect3)), ".")

