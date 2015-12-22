#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""
This Python script can be used to display prayer times in the console. The prayer times are retrieved from islamicfind.org website. To get your own, retrieve the URL from the webiste for you city.

@author: ai8rahim
@license: The MIT License (MIT)
@since: 10.12.2007 (do not change)
"""

import urllib
from sgmllib import SGMLParser
from colorama import Fore, Back, Style
from datetime import datetime

# Parse DOM stuff
#================
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

# Get content from islamicfinder site
#====================================
prayerUrl = 'http://www.islamicfinder.org/prayerDetail.php?country=australia&city=perth_city&state=08&zipcode=〈='
sock = urllib.urlopen(prayerUrl)
html = sock.read()
sock.close()

parser = TBLParser()
parser.feed(html)
parser.close()

# Format output
#==============
for rc, row in enumerate(parser.rows):
	for cc, col in enumerate(row):
		if (rc==1):
			# table header
			cstyle=Fore.BLACK+Back.LIGHTWHITE_EX
		else:
			pray_now = False
			if (row[0]==str(datetime.now().day)):
				# today row
				cstyle=Fore.RED
				if (cc > 1):
					# current prayer time
					current_time = datetime.now()
					p_h, p_m = col.split(':')
					n_h, n_m = row[cc+1].split(':') if (cc+1) != len(row) else col.split(':')
					cprayer_time = current_time.replace(hour=int(p_h), minute=int(p_m))
					nprayer_time = current_time.replace(hour=int(n_h), minute=int(n_m))
					if (current_time >= cprayer_time) and (current_time < nprayer_time):
						pray_now = True
					else:
						pray_now = False
			else:
				# alternating rows foreground
				if (rc%2==0):
					cstyle=Fore.WHITE
				else:
					cstyle=Fore.BLACK
			# alternating rows background
			if (pray_now == True):
				cstyle+=Back.BLUE
			elif (rc%2==0):
				cstyle+=Back.LIGHTBLACK_EX
			else:
				cstyle+=Back.WHITE
		print(cstyle+("{0:5.5s}".format(col))),
	print "\n"

