from googleapiclient.discovery import build
import re
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser
import urllib3
from urllib.parse import urlparse, parse_qs


DEVELOPER_KEY = "AIzaSyC8Lr1783Le0ZFz_rJ_wFTLzJlTdQXpxYM"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
def youtube_search(q, max_results=50, order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=q,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=max_results,
        location=location,
        locationRadius=location_radius
     ).execute()
    return search_response['items'][0]

def parse_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None


import httplib2
import os
import sys
import json

from googleapiclient.discovery import build_from_document
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "./client_secret_....json"

YOUTUBE_READ_ONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """WARNING: Please configure OAuth 2.0
    To make this sample run you will need to populate the client_secrets.json file found at: %s with information from the APIs Console https://console.developers.google.com
    For more information about the client_secrets.json file format, please visit: https://developers.google.com /api-client-library/python/guide/aaa_client_secrets""" % os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_ONLY_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    with open("youtube-v3-discoverydocument.json", "r", encoding="utf8") as f:
        doc = f.read()
        return build_from_document(doc, http=credentials.authorize(httplib2.Http()))

def get_comment_threads(youtube, video_id):
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText"
    ).execute()
    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
    return results["items"]


def get_comments(youtube, parent_id):
    results = youtube.comments().list(
        part="snippet",
        parentId=parent_id,
        textFormat="plainText"
    ).execute()

    for item in results["items"]:
        author = item["snippet"]["authorDisplayName"]
        text = item["snippet"]["textDisplay"]
        print("Comment by " + author + ": " + text)

    return results["items"]

if __name__ == '__main__':
    # The "videoid" option specifies the YouTube video ID that uniquely
    # identifies the video for which the comment will be inserted.
    argparser.add_argument("videoid", help="Required; ID for video for which the comment will be inserted.")
    # The "text" option specifies the text that will be used as comment.
    #argparser.add_argument("--text", help="Required; text that will be used as comment.")
    args = argparser.parse_args()

    if not args.videoid:
        exit("Please specify videoid using the --videoid= parameter.")

    youtube = get_authenticated_service(args)
    # All the available methods are used in sequence just for the sake of an example.
    try:
        video_comment_threads = get_comment_threads(youtube, args.videoid)
        parent_id = video_comment_threads[0]["id"]
        video_comments = get_comments(youtube, parent_id)

    except HttpError as e:
        print("An HTTP error " + str(e.resp.status) + " occurred:\n" +  json.dumps(str(e.content)))
    else:
        print("Inserted, listed, updated, moderated, marked and deleted comments.")
