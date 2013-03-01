#!/usr/bin/env python

import urllib
import urllib.request as url
import sys

args = sys.argv
help_str = "Usage: " + args[0] + " [search]. Search youtube for a video."

if len( args ) > 1:
	search = "http://youtube.com/results?search_query=" + " ".join( args[1:] )
	search = search.replace( " ", "+" )
	youtube = url.urlopen( search )
	data = str( youtube.read( ))
	vids = []

	title = ""
	views = ""
	link  = ""
	vid_id = ""

	for thing in data.split( "\\n" ):
		if "yt-lockup2-video" in thing and "event=ad" not in thing:
			vids.append( thing )

	if len( vids ) < 1:
		exit(0)

	for vid in vids:
		i = 0
		metadata = vid.split("\"")
		for thing in metadata:
			if thing == " data-context-item-title=":
				title = metadata[i+1]
			elif thing == " data-context-item-id=":
				vid_id = metadata[i+1]
			elif thing == " data-context-item-views=":
				views = metadata[i+1]
			if ( i < len( metadata ) - 1 ):
				i+=1
			
		link = "http://youtube.com/watch?v=" + vid_id

		title = title.replace( "&", "" )
		title = title.replace( "amp;", "&" )
		title = title.replace( "quot;", "\"")

		msg = link
		msg = title + ": " + msg
		msg += " (" + views + ")"

		print( msg );

else:
	print( help_str );
