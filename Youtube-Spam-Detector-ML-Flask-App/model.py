import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
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

# comment text vectorization
corpus = df_x
cv = CountVectorizer()
X = cv.fit_transform(corpus)

# Model Fitting (Naive Bayes)
X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.3, random_state=7)
clf = MultinomialNB()
clf.fit(X_train,y_train)
print("Accuracy of Model", clf.score(X_test, y_test)*100, "%")

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



naivebayesML = open("YtbSpam_model.pkl","wb")
pickle.dump((clf, cv), naivebayesML)
naivebayesML.close()

# example prediction 3 using packaged model
ytb_model = open("YtbSpam_model.pkl","rb")
new_model = pickle.load(ytb_model)
comment3 = ["Definitely my favorite music video by this artist."]
vect3 = cv.transform(comment3).toarray()
print(comment3, " is ", isSpam(clf.predict(vect3)), ".")

