#!/usr/bin/env python

import urllib
import urllib.request as url
import sys
import optparse
import re

site = "https://aur.archlinux.org"
def_format="{title}: {link}"

categoryDict = {
	"any"		: "0",
	"daemons"	: "2",
	"devel"		: "3",
	"editors"	: "4",
	"emulators"	: "5",
	"games"		: "6",
	"gnome"		: "7",
	"i18n"		: "8",
	"kde"		: "9",
	"kernels"	: "19",
	"lib"		: "10",
	"modules"	: "11",
	"multimedia"	: "12",
	"network"	: "13",
	"office"	: "14",
	"science"	: "15",
	"system"	: "16",
	"x11"		: "17",
	"xfce"		: "18"
}

if __name__ == "__main__":
	help_str = "Usage: meh [search]. Search the Arch User Repository for a package."
	parser = optparse.OptionParser( "Usage: %prog [options] query" )

	parser.add_option( 	"-c", "--category", dest="category", default="any", type="string",
				help="Category to search. Valid options: " + ", ".join( categoryDict.keys( )))

	parser.add_option( 	"-b", "--searchby", dest="searchby", default="nd", type="string",
				help="What to search for. \"n\"=name only, \"x\"=exact name, \"m\"=maintainer, " +
				     "\"s\"=submitter, \"d\"=description. Default is \"nd\"." )

	parser.add_option(	"-k", "--keywords", dest="keywords", default=False, type="string",
				help="Keywords to search for. This is usually specified by the command line " + 
				     "args, but if you want to list them explicitly, this is for you." )

	parser.add_option( 	"-o", "--outdated", dest="outdated", default="", type="string",
				help="\"on\" to allow for outdated packages, \"off\" to disallow them." )

	parser.add_option( 	"-s", "--sort", dest="sort", default="", type="string",
				help="How results should be sorted. \"n\"=name, \"c\"=category, \"v\"=votes, " +
				     "\"w\"=voted, \"o\"=notify, \"m\"=maintainer, \"a\"=age." )

	parser.add_option(	"-d", "--order", dest="order", default="a", type="string",
				help="How to sort results. \"a\"=ascending, \"d\"=decending." )

	parser.add_option(	"-p", "--perpage", dest="perpage", default="50", type="string",
				help="How many results to display per page. This utility only displays the first " +
				     "page, so this also states the max results to be output. Note: Only 50, 100, " +
				     "and 250 are valid." )

	parser.add_option( 	"-f", "--offset", dest="offset", default="0", type="string",
				help="How many results to offset by." )

	parser.add_option( 	"-O", "--doorphins", dest="orphins", action="store_true", default=False,
				help="Show only orphined packages." )

	parser.add_option( 	"-F", "--format", dest="format", default=def_format,
				help="The output format string. This is a python format string. Variables passed " + 
				     "to format are \"title\", \"link\", \"tarball\", \"votes\", \"version\", " +
				     "\"category\", and \"maintainer\". " +
				     "Default is " + "\"" + def_format + "\"." )

	parser.add_option(	"-D", "--debug", dest="debug", action="store_true", default=False,
				help="Show debug output" )

	(options, args) = parser.parse_args()
	

	if len( args ) >= 1 or options.keywords:
		if not options.keywords:
			s_string = "+".join( args )
		else:
			s_string = options.keywords.replace( " ", "+" )

		if options.category.lower() not in categoryDict:
			print( "\"" + options.category + "\" is not a valid category." )
			exit( 1 )

		query = "O=%s&C=%s&SeB=%s&K=%s&outdated=%s&SB=%s&SO=%s&PP=%s" % \
			( options.offset, categoryDict[ options.category.lower() ], options.searchby, s_string, \
			  options.outdated, options.sort, options.order, options.perpage )

		if options.orphins:
			query += "&do_Orphans=Orphans"

		search = site + "/packages/?" + query

		if options.debug:
			print( "Search string: " + search )

		aur = url.urlopen( search )
		data = str( aur.read( ))
		results = data.split( "\\n" )
		i = 0

		for thing in results:
			blarg = re.match( ".*<td><a href=\"/packages.*>.*</a></td>", thing )

			if blarg:
				thing = thing.replace( "\\t", "" )
				title = re.sub( "<.*?>", "", thing )
				link  = site + re.sub( "<.*?\"|/\".*", "", thing )
				tar   = site + "/packages/" + title[:2] + "/" + title + "/" + title + ".tar.gz"

				categ =   re.sub( "<.*?>", "", results[i-1] ).replace( "\\t", "" )
				version = re.sub( "<.*?>", "", results[i+1] ).replace( "\\t", "" )
				votes =   re.sub( "<.*?>", "", results[i+2] ).replace( "\\t", "" )
				descr =   re.sub( "<.*?>", "", results[i+3] ).replace( "\\t", "" )
				maint =   re.sub( "<.*?>", "", results[i+5] ).replace( "\\t", "" )

				out = options.format.format( title=title, link=link, tarball=tar, version=version, 
					votes=votes, category=categ, description=descr, maintainer=maint  )

				out = out.replace( "\\t", "\t" )
				out = out.replace( "\\n", "\n" )
				out = out.replace( "\\v", "\v" )
				out = out.replace( "\\a", "\a" )

				print( out )
			i+=1

		if options.debug:
			print( "Done." )

	else:
		parser.error( "Need arguments, try --help." )
