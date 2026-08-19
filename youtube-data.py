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
        part='snippet',
        id=mv
    )

    response = request.execute()

    return response

###  MAIN SCRIPT EXECUTION  ###
parser = argparse.ArgumentParser()
parser.add_argument("music_video")
args = parser.parse_args()
music_vid = args.music_video
# my_data = youtube_qry('38xYeot-ciM')
my_data = youtube_qry(music_vid)
print("Playlist response output:")
print(my_data)
