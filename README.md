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
	title: text (song title)
	artist: text
	description: text
	publishedDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
	updatedDate: text [formatted as "YYYY-MM-DD HH:MM:SS.SSS"]
	gender: text ["girl group", "boy group", "solo female", "sole male", "mixed", "other"]
	genre: text ["kpop", "kindie", "khiphop", "krock"]
	type: text ["music video", "music show", "fancam", "performance", "live", "practice"]
	numPlays: integer

playlist
	themePlaylist: text	# The playlist ID
	playlistTitle: text	# playlist title
	playlistDescription: text	# playlist description
	playlistPlays: integer	# Number of plays
	playlistUpdated: text	# When the info was pulled from YT YYYY-MM-DD HH:MM:SS.SSS

