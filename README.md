# DB Utils

## Summary
Some companion utilities for kpop_monday_playlist_builder. We are going to gather and save various stats related to the playlists in a sqlite database.

## Tools

### kpop_db_util.py
usage: kpop_db_util.py [-h] [-t] [-m] json_file

### youtube-data.py
usage: youtube-data.py [-h] music_video

### playlist-data.py
Extracts the list of videos from YT API and populates the database
usage: playlist-data.py [-h] playlist_id date theme
Example: playlist-data.py PLMNs4SFWfYno 2026-10-19 CoolCollabs


## Database Schema
* theme
	+ themeId: text (example: "setmefree20260803")
	+ themeName: text
	+ themeDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
	+ themePlaylist: text
	+ playlistPlays: integer	# Number of plays
	+ playlistUpdated: text	# When the info was pulled from YT YYYY-MM-DD HH:MM:SS.SSS

* mv_theme
	+ musicVideoID: text (YouTube MV ID)
	+ themeID: text (themeID in which this MV appears)
+
* musicvideo
	+ MV_ID: text (YouTube MV ID)
	+ title: text (song title)
	+ artist: text
	+ description: text
	+ publishedDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
	+ updatedDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
	+ gender: integer ["1 (boy group)", "2 (girl group)", "3 (sole male)", "4 (solo female)", "5 (mixed)", "6 (other)"]
	+ genre: integer [1 (k-pop)", "2 (k-indie)", "3 (k-hiphop)", "4 (k-rock)]
	type: integer ["1 (MV)", "2 (performance)", "3 (music show)", "4 (fancam)", "5 (live)", "6 (practice)", "7 (audio only)", "8 (soundtrack)"]
	+ numPlays: integer
+
* playlist [I DON'T THINK THIS IS NEEDED. OVERLAPS "theme"]
	+ themePlaylist: text	# The YT playlist ID (example: "PLG9eH70lDCno")
	+ playlistTitle: text	# playlist title (example: "SetMeFree")
	+ playlistDescription: text	# playlist description (optional)
	+ playlistPlays: integer	# Number of plays
	+ playlistUpdated: text	# When the info was pulled from YT YYYY-MM-DD HH:MM:SS.SSS
+
* gender (lookup table to convert integer to readable gender)
	+ index: integer
	+ gender: text
+
* genre (lookup table to convert integer to readable genre)
	+ index: integer
	+ genre: text
+
* type (lookup table to convert integer to readable type)
	+ index: integer
	+ type: text
+