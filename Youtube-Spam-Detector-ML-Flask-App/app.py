from flask import Flask,render_template, request
from sklearn.externals import joblib
from oauth2client.tools import argparser
import argparse
import youtube as yt

app = Flask(__name__, static_url_path='')

@app.route('/home/')
def root():
    return app.send_static_file('home.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    ytb_model = open("YTSpam_model.pkl", "rb")
    (clf, cv) = joblib.load(ytb_model)
    if request.method == 'POST':
        comment = request.form['comment']
        data = [comment]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)
    return render_template('prediction.html', prediction= my_prediction)

@app.route('/back',methods=['POST'])
def back():
    return render_template('home.html')

@app.route('/submit', methods = ['POST'])
def submit():
    ytb_model = open("YTSpam_model.pkl", "rb")
    (clf, cv) = joblib.load(ytb_model)
    if request.method == 'POST':
        id = yt.parse_video_id(request.form['comment'])
        (authors, comments) = yt.get_comment_threads(id)
        spam_comments = []
        for elem in range(0, len(comments)):
            vect = cv.transform([comments[elem]]).toarray()
            my_prediction = clf.predict(vect)
            if my_prediction == 1:
                spam_comments.append((authors[elem], comments[elem]))
        print(spam_comments)
    return render_template('comments.html',comments = spam_comments)

if __name__ == '__main__':
    app.run(debug=True)