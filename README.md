# DB Utils

Some companion utilities for kpop_monday_playlist_builder. We are going to gather and save various stats related to the playlists in a sqlite database.

## Schema
* theme
	+ themeId: text
	+ themeName: text
	+ themeDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
	+ themePlaylist: text
+
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
	type: integer ["1 (MV)", "2 (performance)", "3 (music show)", "4 (fancam)", "5 (live)", "6 (practice)"]
	+ numPlays: integer
+
* playlist
	+ themePlaylist: text	# The playlist ID
	+ playlistTitle: text	# playlist title
	+ playlistDescription: text	# playlist description
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
