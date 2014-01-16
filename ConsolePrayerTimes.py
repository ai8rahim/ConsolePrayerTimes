#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""
This Python script can be used to display prayer times in the console. The prayer times are retrieved from islamicfind.org website. To get your own, retrieve the URL from the webiste for you city.

@author: ai8rahim
@contact: mr.ahmedibrahim@gmail.com
@copyright: Copyright (c) 2014 Ahmed Ibrahim
@license: The MIT License (MIT)
@requires: python version 2.6.6
@since: 10.12.2007 (do not change)
@date: 16.01.2014
@version: 0.2

"""

import urllib
from sgmllib import SGMLParser

class TBLParser(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.doit = 0
		self.cols = []
		self.rows = []
	
	def start_td(self, attrs):
		for k, v in attrs:
			if attrs == [('class', 'IslamicData'), ('bgcolor', '#FFFFFF'), ('align', 'center')] or \
				attrs == [('class', 'IslamicData'), ('bgcolor', '#FFFFCC'), ('align', 'center')]:
				self.doit = 1
	
	def end_td(self):
		self.doit = 0
	
	def handle_data(self, text):
		if self.doit == 1:
			self.cols.append(text)
			if len(self.cols)%8 == 0:
				self.rows.append(self.cols)
				self.cols = []

prayerUrl = 'http://www.islamicfinder.org/prayerDetail.php?country=australia&city=perth_city&state=08&zipcode=〈='
sock = urllib.urlopen(prayerUrl)
html = sock.read()
sock.close()

parser = TBLParser()
parser.feed(html)
parser.close()

for row in parser.rows:
	for col in row:
		print "%5.5s" % col,
	print "\n"


