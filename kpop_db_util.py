# Utility to update the kpop monday database
#
# usage: python kpop_db_util.py <filename.json>
#

import json
import os
import sys
import re
import argparse
import sqlite3

sqlite_db = '/var/sqlite/kpop_monday.db'
connection = sqlite3.connect(sqlite_db)

# Function to update theme table
def update_theme_table(json_file):

    with open(json_file, "r") as file:
        data = json.load(file)

    theme = data["theme"]
    playlistID = data["playlistID"]
    pl_date = data["date"]
    theme_vids = data["theme_vids"]

    # need to remove "-" from pl_date
    pl_date_bare=pl_date.replace("-", "")
    newThemeId=theme.lower() + pl_date_bare

    # make sure themeId not already present
    cursor = connection.cursor()
    bool = cursor.execute(
        "SELECT COUNT(*) from theme WHERE themeId=?",
        (newThemeId,)
    ).fetchone()
    print(bool[0])
    if bool[0] > 0:
        print("themeId ", newThemeId, "already present in theme table. Nothing to add.")
    else:
        res = "INSERT INTO theme VALUES('{}', '{}', '{}', '{}');".format(newThemeId, theme, pl_date_bare, playlistID)
        print(res)
        # Write directly to the database:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO theme VALUES(?,?,?,?)", (newThemeId, theme, pl_date_bare, playlistID))
        connection.commit()

# Function to update mv_theme table
def update_mv_theme_table(json_file):

    with open(json_file, "r") as file:
        data = json.load(file)

    theme = data["theme"]
    playlistID = data["playlistID"]
    pl_date = data["date"]
    theme_vids = data["theme_vids"]

    # need to remove "-" from pl_date
    pl_date_bare=pl_date.replace("-", "")
    newThemeId=theme.lower() + pl_date_bare

    for mv in theme_vids:
        # make sure themeId not already present
        cursor = connection.cursor()
        bool = cursor.execute(
            "SELECT COUNT(*) from mv_theme WHERE musicVideoID=? AND themeId=?",
            (mv, newThemeId,)
        ).fetchone()
        print(bool[0])
        if bool[0] > 0:
            print("musicVideoID", mv, "with themeId ", newThemeId, "already present in table. Nothing to add.")
        else:
            res = "INSERT INTO mv_theme VALUES('{}', '{}');".format(mv, newThemeId)
            print(res)
            # Write directly to the database:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO mv_theme VALUES(?,?)", (mv, newThemeId))
            connection.commit()

###  MAIN SCRIPT EXECUTION  ###
parser = argparse.ArgumentParser()
parser.add_argument("json_file")
parser.add_argument("-t", "--theme", help="update theme table from json file", action="store_true")
# This will be implemented later
parser.add_argument("-m", "--mv", help="update mv_theme table from json", action="store_true")
args = parser.parse_args()
json_file = args.json_file

if args.theme:
    update_theme_table(json_file)

if args.mv:
    update_mv_theme_table(json_file)
