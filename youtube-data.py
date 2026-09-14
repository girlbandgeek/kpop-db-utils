# Pull selected statuses with Mastodon API and process them
# from mastodon import Mastodon
import argparse
import datetime
from datetime import date
from datetime import timedelta
from datetime import time
from dateutil import parser
from dotenv import load_dotenv
import os
import sys
import re
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build

# Define some variables
# I have created an api key. This may supersede the Oauth stuff.

load_dotenv()
api_key=os.getenv("yt_api_key")

# Google API related:
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Function to query music video data from YouTube
def youtube_qry(mv):

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        # part='snippet,contentDetails,statistics',
        # part='snippet',
        part='snippet,statistics',
        id=mv
    )

    response = request.execute()

    # Explore the layout of the YT response
    for key, value in response.items():
        print("key: ", key)
        print("value: ", response[key])
        print("items type: ", type(response[key]))
        print()

    # Let's unpack response["items"][0]
    item_dict=response["items"][0]
    print("Unpacking the inner dict of items")
    # print(type(item_dict))

    for kkey, vvalue in item_dict.items() :
        print("key: ", kkey)
        print("value: ", vvalue)

    # Let's unpack the snippet
    snippet_dict=response["items"][0]["snippet"]
    print()
    print("Unpacking the snippet")
    for kkey, vvalue in snippet_dict.items() :
        print("key: ", kkey)
        print("value: ", vvalue)

    # Here is placeholder for extracting the db fields
    print()
    print("Extract the desired fields")
    ref_url='https://www.youtube.com/watch?v='+mv
    print("Reference url: ", ref_url)
    # title: text (song title)
    # artist: text
    # description: text
    t_title=response["items"][0]["snippet"]["title"]
    print("Title: ", t_title)
    # publishedDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
    t_publishedDate=response["items"][0]["snippet"]["publishedAt"]
    c_publishedDate=datetime.datetime.strptime(t_publishedDate, "%Y-%m-%dT%H:%M:%SZ")
    print("publishedDate: ", c_publishedDate)
    # updatedDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
    t_updatedDate=datetime.datetime.now()
    print("updatedDate: ", t_updatedDate)
    # gender: text ["girl group", "boy group", "solo female", "sole male", "mixed", "other"]
    # genre: text ["k-pop", "k-indie", "k-hiphop", "k-rock"]
    # type: text ["music video", "music show", "fancam", "performance", "live", "practice"]
    # numPlays: integer
    t_numPlays=response["items"][0]["statistics"]["viewCount"]
    print("numPlays: ", t_numPlays)


    return response

###  MAIN SCRIPT EXECUTION  ###
parser = argparse.ArgumentParser()
parser.add_argument("music_video")
args = parser.parse_args()
music_vid = args.music_video
# my_data = youtube_qry('38xYeot-ciM')
my_data = youtube_qry(music_vid)
# print("Playlist response output:")
# print(my_data)
