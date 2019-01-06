from flask import Flask,render_template,url_for,request
from sklearn.externals import joblib


app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)