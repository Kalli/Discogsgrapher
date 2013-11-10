#!/usr/bin/python
# -*- coding: utf-8 -*
import releaseparser
import releasenetwork
import argparse

description = '''
		This script creates an artist/label network from a Discogs.com release data dump file and and exports it in a d3 formatted json graph file. 
		For more information see http://www.github.com/kalli/discogsgrapher
		Live demo at http://www.karltryggvason.com/discogsgrapher
	'''
argsparser = argparse.ArgumentParser(description=description)
argsparser.add_argument("-x", "--xmlfile", type=str, help="/full/path/to/discogs/data/dump/release.xml")
argsparser.add_argument("-c", "--country", type=str, help="The country of the releases")
argsparser.add_argument("-s", "--style", type=str, help="The style that you want to parse a network for")
argsparser.add_argument("-t", "--threshold", type=int, help="The treshold (minum number of releases) that artists must have in this style to be included")
argsparser.add_argument("-b", "--begin", type=int, help="the year you want to begin parsing from")
argsparser.add_argument("-e", "--end",  type=int, help="the year you want to begin parsing from")
args = argsparser.parse_args()
parser = releaseparser.ReleaseParser(args.xmlfile, args.style, args.threshold, args.country, args.begin, args.end)
network = releasenetwork.ReleaseNetwork(parser)
network.saveGraphAsJson()