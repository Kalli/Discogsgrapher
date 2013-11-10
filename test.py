#!/usr/bin/python
# -*- coding: utf-8 -*
import releaseparser
import releasenetwork
import unittest

class Test1(unittest.TestCase):
	def setUp(self):
		xmlfile = "./test-releases.xml"
		style = "test"
		threshold = 1
		start = 2004
		end = 2006
		country = "UK"
		self.parser = releaseparser.ReleaseParser(xmlfile, style, threshold, country, start, end)


	def testReleaseParser(self):
		self.assertEqual(len(self.parser.artists),3)
		self.assertEqual(len(self.parser.labels),2)

	def testReleaseNetwork(self):
		network = releasenetwork.ReleaseNetwork(self.parser)
		self.assertEqual(network.g.number_of_nodes(),3)
		self.assertEqual(network.g.number_of_edges(),5)

if __name__ == '__main__':
    unittest.main()