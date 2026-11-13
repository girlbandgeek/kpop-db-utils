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

# How many results to return from YouTube api (max = 50)
myMaxResults=20

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

    # define a results list
    result_list=[]

    # Pull the first page of results; find total playlist video count
    initialRequest = youtube.playlistItems().list(
    # part="contentDetails","snippet"
    part="contentDetails",
    maxResults=myMaxResults,
    playlistId=pl,
    )

    initialResponse = initialRequest.execute()

    initial_item_list=initialResponse["items"]
    print("Unpacking the list of music videos")

    for vvalue in initial_item_list :
        # print(vvalue["contentDetails"]["videoId"])
        result_list.append(vvalue["contentDetails"]["videoId"])

    myTotalResults = initialResponse["pageInfo"]["totalResults"]
    print("myTotalResults: ", myTotalResults)

    # Check the number of items in the playlist. If it's less the page size
    # We can retrieve it in one go:
    if myTotalResults <= myMaxResults :
        return result_list
    else:

        # Playlist is longer than playlist. Loop thru to retrieve all videos:
        myPageToken = initialResponse["nextPageToken"]
        print("myPageToken: ", myPageToken)

        while len(result_list) < myTotalResults :

            request = youtube.playlistItems().list(
                # part="contentDetails","snippet"
                part="contentDetails",
                maxResults=myMaxResults,
                playlistId=pl,
                pageToken=myPageToken
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

            item_list=response["items"]
            print("Unpacking the list of music videos")

            for wvalue in item_list :
                # print(vvalue["contentDetails"]["videoId"])
                if wvalue["contentDetails"]["videoId"] in result_list :
                    print("Video ", wvalue, "already in result_list")
                else:
                    print("Adding ", wvalue, "to result_list")
                    result_list.append(wvalue["contentDetails"]["videoId"])

            # If we get nextPageToken value, retrieve the next page.
            # Otherwise, we're done and the while loop can end.
            try:
                myPageToken = response["nextPageToken"]
                print("myPageToken: ", myPageToken)
            except:
                print("nextPageToken value not returned.")

            print("Length of result_list: ", len(result_list))

    return result_list

# Function to update mv_theme table
# taken from kpop_db_util.py and modified as appropriate
def update_mv_theme_table(myThemeId, mv_list):

    for mv in mv_list:
        # make sure themeId not already present
        cursor = connection.cursor()
        bool = cursor.execute(
            "SELECT COUNT(*) from mv_theme WHERE musicVideoID=? AND themeId=?",
            (mv, myThemeId,)
        ).fetchone()
        print(bool[0])
        if bool[0] > 0:
            print("musicVideoID", mv, "with themeId ", myThemeId, "already present in table. Nothing to add.")
        else:
            res = "INSERT INTO mv_theme VALUES('{}', '{}');".format(mv, myThemeId)
            print(res)
            # Write directly to the database:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO mv_theme VALUES(?,?)", (mv, myThemeId))
            connection.commit()

###  MAIN SCRIPT EXECUTION  ###
parser = argparse.ArgumentParser()
parser.add_argument("playlist")
parser.add_argument("themeId")
args = parser.parse_args()
# parser.add_argument("my_date")
# parser.add_argument("my_theme")
my_playlist = args.playlist
my_theme_Id = args.themeId
my_data = playlist_qry(my_playlist)
print(my_data)
print("Total number of videos: ", len(my_data))

input_aa = input('Do you want to update mv_theme table? y/n: ')
if (input_aa.lower()).startswith("y"):
    update_mv_theme_table(my_theme_Id, my_data)
else:
    print("mv_theme table will not be updated. exiting.")
    sys.exit()
