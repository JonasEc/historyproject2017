#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the links for all MCPs
# 2017 07 07


#########################
# "administrative stuff"

from __future__ import division

import mechanize
import cookielib 

import pandas as pd
from bs4 import BeautifulSoup
from os import chdir
import re
from unidecode import unidecode
from math import ceil
import time
import sys
from random import random 


######################
# Executive Decisions

### how many records max per search type?
maxPage = 76
entries = 20


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our output?
output = []
outputClass= "input/MCLinks/MCPLinksNew"
csv = ".csv"

nameCSV = raw_input("DataSetName")

rangeInputLower = raw_input("What lower name?")
rangeInputLower = int(rangeInputLower)
rangeInputUpper = raw_input("What upper name?")
rangeInputUpper = int(rangeInputUpper)

######################
# Mechanize Set up

#  set up the browser
driver = mechanize.Browser()

# Enable cookie support for mechanize 
cookiejar = cookielib.LWPCookieJar() 
driver.set_cookiejar( cookiejar ) 

# Broser options 
driver.set_handle_equiv( True ) 
driver.set_handle_gzip( True ) 
driver.set_handle_redirect( True ) 
driver.set_handle_referer( True ) 
driver.set_handle_robots( False ) 

# # this does seomthing ...  (copy paste from stackexchange...)
driver.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
driver.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 



######################
# THE SEARCH SET UP

# base URL for the search: we will then loop thru "all" pages (up to max)

# https://search.livesofthefirstworldwar.org/search/world-records/surrey-recruitment-registers-1908-1933?firstname=adam&o=yearofbirth
# https://search.livesofthefirstworldwar.org/search/world-records/surrey-recruitment-registers-1908-1933?firstname=adam&o=yearofbirth&_=1495390374398&d=asc
# &page=
baseurl = "https://search.livesofthefirstworldwar.org/search/world-records/manchester-regiment-city-battalions-1914-1916?unit="


unitList = [str(bat) + "bn.%20" + column + "%20co.%20plat.%20" + str(platoon) for bat in range(16,24) for column in ["A", "B", "C", "D", "E"] for platoon in range(1,21)]

unitListTrunc = unitList[rangeInputLower:rangeInputUpper]

############## LOOP THRU ALL NAMES ##################

# try:
for unit in unitListTrunc:

# open each webpage individually
	url = baseurl + unit 
	time.sleep(random())
	driver.open(url)
	datasource = driver.response().read()
	datasoup = BeautifulSoup(datasource,"lxml")

## find out what we are dealing with:
	hitsHeader = datasoup.find_all('div', class_ = "SearchResultsHeader")[0]
	hits = hitsHeader.text
	hits = hits.replace(',',"")
	hits = [int(s) for s in hits.split() if s.isdigit()]

	if len(hits) == 0:
		continue
	elif hits[0] == 0:
		continue
	else:
### if there are some hits, start scraping!
		maxPageName = min(int(ceil(hits[0]/entries)),maxPage)
		for page in range(0,maxPageName):
			urlNow = url + "&page=" + str(page)
			while True:
				try:
					sleep(random())
					driver.open(urlNow) #if fail, wait 3min
					break
				except:
					time.sleep(180)
	
			datasource = driver.response().read()
			datasoup = BeautifulSoup(datasource,"lxml")
# find the table that has the entire list of search results and save all its rows
			data_rows = datasoup.find_all('tbody')[0].find_all('tr')[0:]

############ then loop over all search results on each page
			for i in range(len(data_rows)):
				dataDs = data_rows[i].find_all('td')
				# get the link to the transcription
				link = dataDs[7].a.get('href')
				link = "https://search.livesofthefirstworldwar.org" + link # complete the link
				# save the link to a csv to use later
				output.append(link) 



### now we use the panda operation data frame to turn our output list into a df
outputframe = pd.DataFrame(output, columns=["Links"])	
outputfile = outputClass + nameCSV + csv ### we need to make a new file name for each save!
### and export that frame to a csv
outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

print 'done! :)'
