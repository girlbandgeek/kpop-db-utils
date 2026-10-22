# Extract playlist data from YouTube API and provides
# functions to update the database
#
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
import sqlite3


# Handle sqlite date conversion
# Define the Adapter (Python object -> SQLite string)
def adapt_datetime(val):
    return val.replace(tzinfo=None).isoformat()

# Define the Converter (SQLite string -> Python object)
def convert_datetime(val):
    # Convert ISO 8601 datetime to datetime.datetime object
    return datetime.datetime.fromisoformat(val.decode())

# register datetime adapters:
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)

sqlite_db = '/var/sqlite/kpop_monday.db'
# sqlite_db = '/var/sqlite/kpop_monday_new.db'
connection = sqlite3.connect(sqlite_db, detect_types=sqlite3.PARSE_COLNAMES)

# Define some variables
# I have created an api key. This may supersede the Oauth stuff.

load_dotenv()
api_key=os.getenv("yt_api_key")

# Google API related:
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

### FUNCTIONS ###
# Function to query playlist data from YouTube
def playlist_qry(pl):

    youtube = build('youtube', 'v3', developerKey=api_key)

    # Will need to put this in a loop, and pass the
    request = youtube.playlistItems().list(
        # part="contentDetails","snippet"
        part="contentDetails",
        maxResults=50,
        playlistId=pl
    )

    response = request.execute()
    # Explore the layout of the YT response


    '''
    print("Explore keys/values in YT response")
    print()
    for key, value in response.items():
        print("key: ", key)
        print("value: ", response[key])
        print("items type: ", type(response[key]))
        print()

    '''
    # define a results list
    result_list=[]
    item_list=response["items"]
    print("Unpacking the list of music videos")

    for vvalue in item_list :
        # print(vvalue["contentDetails"]["videoId"])
        result_list.append(vvalue["contentDetails"]["videoId"])



    return result_list

###  MAIN SCRIPT EXECUTION  ###
parser = argparse.ArgumentParser()
parser.add_argument("playlist")
args = parser.parse_args()
# parser.add_argument("my_date")
# parser.add_argument("my_theme")
my_playlist = args.playlist
my_data = playlist_qry(my_playlist)
print(my_data)
print("Total number of videos: ", len(my_data))
