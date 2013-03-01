#!/usr/bin/env python3

import urllib
import urllib.request as url
import re
import sys

if __name__ == "__main__":
	if len( sys.argv ) > 1:
		search = "https://thepiratebay.se/search/" + " ".join( sys.argv[1:] )
		search = search.replace( " ", "%20" )
		tpb = url.urlopen( search )
		data = str( tpb.read( ))
		dsplit = data.split( "\\n" )

		links = []
		stats = [] 
		titles = []

		title = ""
		link  = ""
		i = 0

		for thing in dsplit:
			if "<a href=\"magnet:" in thing:
				links.append( thing )
				titles.append( dsplit[i-2] )
			elif "<td align=\"right\">" in thing:
				stats.append( thing )
			i+=1

		if len( links ) < 1:
			print( "No results." )
			exit( 0 )

		i = 0
		j = 0
		for thing in links:
			metadata = thing.split( "\"" )
			link = metadata[1]
			#print( stats )
			title = re.sub( "<.*?>", "", titles[i] )[6:]
			dat1 =  re.sub( "<.*?>", "", stats[j] )[4:]
			dat2 =  re.sub( "<.*?>", "", stats[j+1] )[4:]

			print( "Seeders: " + dat1 + ", Leechers: " + dat2 + ", title: \"" + title + "\", magnet: \"" + link + "\"" )
			i += 1
			j += 2
	else:
		print( "usage: tpb [search] [limit]" );
