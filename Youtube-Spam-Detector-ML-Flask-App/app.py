from flask import Flask,render_template, request
from sklearn.externals import joblib
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

        parser = argparse.ArgumentParser()
        parser.add_argument("--videoid", dest='videoid', default="L-oNKK1CrnU", help="ID of video to like.")
        args = parser.parse_args()

        youtube = yt.get_authenticated_service(args)

        data = yt.get_comments(youtube, id)
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)
        spam_comments = []
        print (id)
        print (data)
        print (my_prediction)
        for elem in range(0, len(data)):
            if my_prediction[elem] == 1:
                spam_comments.append(data[elem])
    return render_template('comments.html', comment = spam_comments)

if __name__ == '__main__':
    app.run(debug=True)