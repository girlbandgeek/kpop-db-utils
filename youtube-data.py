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
# should be moved to .env variable before committing
api_key = 'AIzaSyBkzhQBGvsPz20aU0QnLBOvhKmSpAJJyas'

# Google API related:
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
# UCP5H3NxIdTebfMG-Iy3vIvQ

'''
    request = youtube.channels().list(
        part='statistics, contentDetails',
        id='UCP5H3NxIdTebfMG-Iy3vIvQ'
        )
'''

# Function to query music video data from YouTube
def youtube_qry(music_video):

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=music_video
    )

    response = request.execute()

    return response

my_data = youtube_qry('38xYeot-ciM')
print("Playlist response output:")
print(my_data)
    


###  MAIN SCRIPT EXECUTION  ###


