DB Utils
Some companion utilities for kpop_monday_playlist_builder. We are going to gather and save various stats related to the playlists in a sqlite database.

Schema
theme
	themeId: text
	themeName: text
	themeDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
	themePlaylist: text

mv_theme
	musicVideoID: text (YouTube MV ID)
	themeID: text (themeID in which this MV appears)

musicvideo
	MV_ID: text (YouTube MV ID)
	title: text
	description: text
	artist: text
	genre: text
	gender: text
	date: text

playlist
	themePlaylist: text	# The playlist ID
	playlistTitle: text	# playlist title
	playlistDescription: text	# playlist description
	playlistPlays: integer	# Number of plays
	playlistUpdated: text	# When the info was pulled from YT YYYY-MM-DD HH:MM:SS.SSS

