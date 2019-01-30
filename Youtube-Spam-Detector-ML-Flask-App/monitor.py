from sklearn.externals import joblib
import argparse
import youtube as yt
from oauth2client.tools import argparser, run_flow

ytb_model = open("YTSpam_model.pkl", "rb")
(clf, cv) = joblib.load(ytb_model)
id = yt.parse_video_id("https://www.youtube.com/watch?v=nqMYG2Riq54&list=PLHEN7nVUglIRGw5xRC4L-RXwudJqyCKlU&index=14")
# The "videoid" option specifies the YouTube video ID that uniquely
  # identifies the video for which the comment will be inserted.
argparser.add_argument("videoid",
    help="Required; ID for video for which the comment will be inserted.")
  # The "text" option specifies the text that will be used as comment.
args = argparser.parse_args()

if not args.videoid:
    exit("Please specify videoid using the --videoid= parameter.")

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