#!/usr/bin/env python3

import urllib
import urllib.request as url
import re
import sys

if __name__ == "__main__":
	if len( sys.argv ) > 1:
		search = "http://www.duckduckgo.com/html/?q=" + " ".join( sys.argv[1:] )
		search = search.replace( " ", "+" )
		ddg = url.urlopen( search )
		data = str( ddg.read( ))
		links = []

		title = ""
		link  = ""

		for thing in data.split( "\\n" ):
			if "<a rel=\"nofollow\" class" in thing:
				links.append( thing )

		if len( links ) < 1:
			print( "No results." )
			exit( 0 )

		for thing in links:
			metadata = thing.split("\"")
			link = metadata[5]
			title = metadata[6][1:]
			title = re.sub( "<.*?>", "", title )

			print( link )
	else:
		print( "usage: ddg [search] [limit]" );
