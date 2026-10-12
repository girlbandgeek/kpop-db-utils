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
import sqlite3

# Handle sqlite date conversion
# Define the Adapter (Python object -> SQLite string)
def adapt_date(val):
    return val.isoformat()

# Define the Adapter (Python object -> SQLite string)
def adapt_datetime(val):
    return val.replace(tzinfo=None).isoformat()

# Define the Converter (SQLite string -> Python object)
def convert_date(s):
    return datetime.date.fromisoformat(s.decode("utf-8"))

def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(val.decode())

# register datetime adapters:
sqlite3.register_adapter(datetime.date, adapt_date)
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("date", convert_date)
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
    # Uncomment below for verbose/redundant output
    '''
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
    '''
    # Here is placeholder for extracting the db fields
    print()
    print("Extracting the desired fields from YouTube API ...")
    # ref_url='https://www.youtube.com/watch?v='+mv
    # print("Reference url: ", ref_url)
    t_title=response["items"][0]["snippet"]["title"]
    print("Title: ", t_title)
    # title: text (song title)
    # my_title = input('Enter song title: ')
    # artist: text
    # my_artist = input('Enter artist name: ')
    # description: text
    # my_description = input('Enter description (optional): ')

    # publishedDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
    t_publishedDate=response["items"][0]["snippet"]["publishedAt"]
    c_publishedDate=datetime.datetime.strptime(t_publishedDate, "%Y-%m-%dT%H:%M:%SZ")
    print("publishedDate: ", c_publishedDate)
    # updatedDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
    # t_updatedDate=datetime.datetime.now()
    # print("updatedDate: ", t_updatedDate)
    # my_gender = input('Enter gender ["1 (boy group)", "2 (girl group)", "3 (sole male)", "4 (solo female)", "5 (mixed)", "6 (other)"]: ')
    # my_genre = input('Enter genre ["1 (k-pop)", "2 (k-indie)", "3 (k-hiphop)", "4 (k-rock)"]: ')
    # my_type = input('Enter type ["1 (MV)", "2 (performance)", "3 (music show)", "4 (fancam)", "5 (live)", "6 (practice"), "7 (audio only)"]: ')
    t_numPlays=response["items"][0]["statistics"]["viewCount"]

    # response = [my_title, my_artist, my_description, c_publishedDate, t_updatedDate, my_gender, my_genre, my_type, t_numPlays]
    response = [t_title, c_publishedDate, t_numPlays]

    return response

# Function to check database for existing data
# def database_qry(mv):
#      return db_contents # list containing db record associated with the requested mv

# Function to update database with enriched data
def db_update(item_list):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE musicvideo SET title = ?, artist = ?, description = ?, publishedDate =?, updatedDate = ?, gender = ?, genre = ?, type = ?, numPlays = ? WHERE MV_ID = ?", (item_list[1], item_list[2], item_list[3], item_list[4], item_list[5], item_list[6], item_list[7], item_list[8], item_list[9], item_list[0])
    )
    connection.commit()
    # return db_result # possibly some kind of status

# Function to update database with updatedDate and numPlays only
def db_update_stats(iitem_list):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE musicvideo SET updatedDate = ?, numPlays = ? WHERE MV_ID = ?", (iitem_list[1], iitem_list[2], iitem_list[0])
    )
    connection.commit()

###  MAIN SCRIPT EXECUTION  ###
parser = argparse.ArgumentParser()
parser.add_argument("music_video")
# parser.add_argument("-u", "--update", help="Update the musicvideo table using data from API", action="store_true")
# parser.add_argument("-s", "--stats", help="Stats. Just update the updatedDate and numPlays from API", action="store_true")
args = parser.parse_args()
music_vid = args.music_video
# my_data = youtube_qry('38xYeot-ciM')

# Retrieve what we have already in the database
cursor = connection.cursor()
mrecord = cursor.execute(
    "SELECT * from musicvideo WHERE MV_ID=?",
    (music_vid,)
).fetchall()
print("Existing contents of k-pop database:")
rrecord=mrecord[0]
print(rrecord)
print()

# Display reference url
ref_url='https://www.youtube.com/watch?v='+music_vid
print("Reference url: ", ref_url)

# Probably will eliminate the arguments to script, and just request input within
# The program:
input_aa = input('Please choose: Update|Edit|Stats|Quit U|E|S|Q: ')

# Populate db fields using API data and user input
# if args.update:
if (input_aa.lower()).startswith("u"):
    my_data = youtube_qry(music_vid)

    my_title = input('Enter song title. Current value {} : '.format(my_data[0])).strip() or my_data[0]
    my_artist = input('Enter artist name: ')
    my_description = input('Enter description (optional): ')
    my_pubDate= input("Enter published date. Current value {} ".format(my_data[1])).strip() or my_data[1]
    tt_updatedDate=datetime.datetime.now()
    # Remove milliseconds
    t_updatedDate = tt_updatedDate.strftime('%Y-%m-%d %H:%M:%S')
    my_updatedDate= input("Enter update date. Current value {} ".format(t_updatedDate)).strip() or t_updatedDate
    my_gender = input('Enter gender ["1 (boy group)", "2 (girl group)", "3 (sole male)", "4 (solo female)", "5 (mixed)", "6 (other)"]: ')
    my_genre = input('Enter genre ["1 (k-pop)", "2 (k-indie)", "3 (k-hiphop)", "4 (k-rock)"]: ')
    my_type = input('Enter type ["1 (MV)", "2 (performance)", "3 (music show)", "4 (fancam)", "5 (live)", "6 (practice"), "7 (audio only)", "8 (soundtrack)"]: ')
    my_numPlays = input("Enter view count. Current value {} ".format(my_data[2])).strip() or my_data[2]

    # print('The following values will be updated.')
    print("Title: ", my_title)
    print("Artist: ", my_artist)
    print("Description: ", my_description)
    print("publishedDate: ", my_pubDate)
    print("updatedDate: ", my_updatedDate)
    print("gender: ", my_gender)
    print("genre: ", my_genre)
    print("type: ", my_type)
    print("numPlays: ", my_numPlays)

    input_bb = input('Do you wish to update db with these values y|n?: ')
    if input_bb == "y":
        print("updating database!")
        db_update([music_vid, my_title, my_artist, my_description, my_pubDate, my_updatedDate, my_gender, my_genre, my_type, my_numPlays])
    else:
        sys.exit()

# Modify the existing fields in the database
elif (input_aa.lower()).startswith("e"):
    print("Edit existing data requested!")
    e_title = input('Enter song title. Current value {} : '.format(rrecord[1])).strip() or rrecord[1]
    e_artist = input('Enter artist name. Current value {} : '.format(rrecord[2])).strip() or rrecord[2]
    e_description = input('Enter (optional) description. Current value {} : '.format(rrecord[3])).strip() or rrecord[3]
    e_pubDate= input('Enter published date. Current value {} : '.format(rrecord[4])).strip() or rrecord[4]
    ttp_updatedDate=datetime.datetime.now()
    # Remove milliseconds
    tp_updatedDate = ttp_updatedDate.strftime('%Y-%m-%d %H:%M:%S')
    e_updatedDate= input('Enter update date. Current value {} '.format(tp_updatedDate)).strip() or tp_updatedDate
    e_gender = input('Enter gender ["1 (boy group)", "2 (girl group)", "3 (sole male)", "4 (solo female)", "5 (mixed)", "6 (other)"]. Current value {} : '.format(rrecord[6])).strip() or rrecord[6]
    e_genre = input('Enter genre ["1 (k-pop)", "2 (k-indie)", "3 (k-hiphop)", "4 (k-rock)"]. Current value {} : '.format(rrecord[7])).strip() or rrecord[7]
    e_type = input('Enter type ["1 (MV)", "2 (performance)", "3 (music show)", "4 (fancam)", "5 (live)", "6 (practice"), "7 (audio only)", "8 (soundtrack)"]. Current value {} : '.format(rrecord[8])).strip() or rrecord[8]
    e_numPlays = input("Enter view count. Current value {} ".format(rrecord[9])).strip() or rrecord[9]

    # print('The following values will be updated.')
    print("Title: ", e_title)
    print("Artist: ", e_artist)
    print("Description: ", e_description)
    print("publishedDate: ", e_pubDate)
    print("updatedDate: ", e_updatedDate)
    print("gender: ", e_gender)
    print("genre: ", e_genre)
    print("type: ", e_type)
    print("numPlays: ", e_numPlays)

    input_cc = input('Do you wish to update db with these values y|n?: ')
    if input_cc == "y":
        print("updating database!")
        db_update([music_vid, e_title, e_artist, e_description, e_pubDate, e_updatedDate, e_gender, e_genre, e_type, e_numPlays])
    else:
        sys.exit()

# This function is not implemented yet!
#if args.stats:
elif (input_aa.lower()).startswith("s"):
    print("Stats update requested!")
    # print("This feature is not implemented yet!")
    me_data = youtube_qry(music_vid)
    utp_updatedDate=datetime.datetime.now()
    # Remove milliseconds
    up_updatedDate = utp_updatedDate.strftime('%Y-%m-%d %H:%M:%S')

    print('The following values will be updated.')
    print("updatedDate: ", up_updatedDate)
    print("numPlays: ", me_data[2])

    input_dd = input('Do you wish to update db with these values y|n?: ')
    if input_dd == "y":
        print("updating database!")
        # db_update_stats
        db_update_stats([music_vid, up_updatedDate, me_data[2]])
    else:
        sys.exit()

# This function is not implemented yet!
elif (input_aa.lower()).startswith("q"):
    print("Exiting youtube-data.py")

else:
    print('Valid options are: Update|Edit|Stats|Quit U|E|S|Q: ')
    print("Exiting youtube-data.py")
