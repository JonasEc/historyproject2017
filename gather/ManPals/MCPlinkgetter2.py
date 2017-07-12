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
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our output?
output = []
outputClass= "input/MCPLinks"
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
baseurl = "https://search.livesofthefirstworldwar.org/search/world-records/manchester-regiment-city-battalions-1914-1916?firstname="

nameList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K" , "L" ,"M" ,"N" , "O", "P", "Q", "R", "S" ,"T" , "U", "V", "W", "X", "Y", "Z"]
nameListTrunc = nameList[rangeInputLower:rangeInputUpper]

variants = "&firstname_variants=true"

yobD = "&o=yearofbirth"
yobA = "&o=yearofbirth&d=asc"

orderAsc = "&o=firstname&d=asc"
orderDsc = "&o=firstname"

############## LOOP THRU ALL NAMES ##################

# try:
for name in nameListTrunc:
	dummy = 0

# open each webpage individually
	url = baseurl + name  + variants + yobA 
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

	if hits[0] > entries*maxPage:
		dummy = 1
	elif hits[0] == 0:
		dummy = 0
	else:
		dummy = 2

### if there are some hits, start scraping!
	if dummy != 0:
		maxPageName = min(int(ceil(hits[0]/entries)),maxPage)
		for page in range(0,maxPageName):
			url = baseurl + name  +  variants + yobA  + "&page=" + str(page)
			try:
				sleep(random())
				driver.open(url) #if fail, wait 3min
			except:
				time.sleep(180)
				driver.open(url) # if fail, wait 5min
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

### if there were loads of hits, we need to do our trick!
		if dummy == 1:
			maxPageName = min(maxPage, int(ceil((hits[0] - entries*maxPage)/entries)))
			for page in range(0,maxPageName):
				url =baseurl + name  + variants + yobD  + "&page=" + str(page)
				try:
					sleep(random())
					driver.open(url) #if fail, wait 3min
				except:
					time.sleep(180)
					driver.open(url) # if fail, wait 5min

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

		if hits[0] > entries*maxPage*2:
			print name +  " in "  + " has many hits: "  + str(hits[0])
			MaxPageName = min(int(ceil(hits[0]/entries)),maxPage)
			for page in range(0,maxPageName):
				url = baseurl + name  + variants + orderAsc  + "&page=" + str(page)
				try:
					sleep(random())
					driver.open(url) #if fail, wait 3min
				except:
					time.sleep(180)
					driver.open(url) # if fail, wait 5min

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

			for page in range(0,maxPageName):
				url = baseurl + name  + variants + orderDsc  + "&page=" + str(page)
				try:
					sleep(random())
					driver.open(url) #if fail, wait 3min
				except:
					time.sleep(180)
					driver.open(url) # if fail, wait 5min

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

# except:
# 	e = sys.exc_info()
# 	print e
# 	print namecounter
# 	print csvcounter
# 	print "error-ed out"

# let me know when its all done
	
print 'done! :)'

