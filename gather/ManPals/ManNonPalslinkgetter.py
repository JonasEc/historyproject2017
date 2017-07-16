#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the links for all ManReg people
# 2017 07 16


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
outputClass= "input/MCLinks/MCNonPals/MCNonPalsLinksYears"
csv = ".csv"

csvcounter = 0
namecounter = 0

# INPUT_SELECTOR:
name = raw_input("DataSetName")

choice = int(raw_input("What townes?"))

rangeInputLower = raw_input("What lower rowlimit?")
rangeInputLower = int(rangeInputLower)
rangeInputUpper = raw_input("What upper rowlimit?")
rangeInputUpper = int(rangeInputUpper)


## malenames
input2 = "input/malefirstnames.csv"


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
 
#####################

def scrape(url,maxPageName):
	output = []
	for page in range(maxPageName):
		urlUse = url + str(page)
		try:
			driver.open(urlUse) #if fail, wait 3min
		except:
			time.sleep(180)
			try:
				driver.open(urlUse) # if fail, wait 3min
			except:
				time.sleep(180)
				try:
					driver.open(urlUse) # if fail, wait 3min 
				except: 
					time.sleep(180)
					driver.open(urlUse)

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
	return output 


######################
# THE SEARCH SET UP

nameList1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K" , "L" ,"M" ,"N" , "O", "P", "Q", "R", "S" ,"T" , "U", "V", "W", "X", "Y", "Z"]

fn = pd.read_csv(input2, sep =',') 
nameList2 = fn["Firstname"].tolist()

nameListChoice = choice*nameList1 + (1- choice)*nameList2


baseurl = "https://search.livesofthefirstworldwar.org/search/world-records/british-army-service-records?regiment=manchester%20regiment&firstname="

yobD = "&o=yearofbirth"
yobA = "&o=yearofbirth&d=asc"

orderAsc = "&o=firstname&d=asc"
orderDsc = "&o=firstname"

birthtownSelector = "&birthtown="

############## LOOP THRU ALL NAMES ##################

# try:
for name in nameListChoice[rangeInputLower:rangeInputUpper]:
	for birthtown in birthtownset:
		dummy = 0

	# open each webpage individually
		url = baseurl + name  + yobA  + year + birthtownSelector + birthtown

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

		if hits[0] > entries*maxPage & hits[0] < entries*maxPage*2:
			dummy = 1
		elif hits[0] == 0:
			continue
		elif hits[0] >= entries*maxPage*2:
			dummy = 2
		else:
			dummy = 0

	### if there are some hits, start scraping!
		maxPageName = min(int(ceil(hits[0]/entries)),maxPage)
		for county in :
			url = baseurl + name  + yobA  + year  + "&page="
		output = output + scrape(url,maxPageName)

	### if there were loads of hits, we need to do our trick!
			if dummy == 1:
				maxPageName = min(maxPage, int(ceil((hits[0] - entries*maxPage)/entries)))
				for page in range(maxPageName):
					url =baseurl + name  + yobD  + year  + "&page=" + str(page)
					try:
						driver.open(url) #if fail, wait 3min
					except:
						time.sleep(180)
						try:
							driver.open(url) # if fail, wait 3min
						except:
							time.sleep(180)
							try:
								driver.open(url) # if fail, wait 3min 
							except: 
								time.sleep(180)
								driver.open(url)
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
				print name +  " in " + year + " has many hits: "  + str(hits[0])
				MaxPageName = min(int(ceil(hits[0]/entries)),maxPage)
				for page in range(0,maxPageName):
					url = baseurl + name  + orderAsc  + year  + "&page=" + str(page)
					try:
						driver.open(url) #if fail, wait 3min
					except:
						time.sleep(180)
						try:
							driver.open(url) # if fail, wait 5min
						except:
							time.sleep(600)
							try:
								driver.open(url) # if fail, wait 1h 
							except: 
								time.sleep(3600)
								driver.open(url)
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
					url = baseurl + name  + orderDsc  + year  + "&page=" + str(page)
					try:
						driver.open(url) #if fail, wait 3min
					except:
						time.sleep(180)
						try:
							driver.open(url) # if fail, wait 5min
						except:
							time.sleep(600)
							try:
								driver.open(url) # if fail, wait 1h 
							except: 
								time.sleep(3600)
								driver.open(url)
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
outputfile = outputClass + name + csv ### we need to make a new file name for each save!
### and export that frame to a csv
outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')
output = [] # and clear for next save
		


# except:
# 	e = sys.exc_info()
# 	print e
# 	print namecounter
# 	print csvcounter
# 	print "error-ed out"

# let me know when its all done
	
print 'done! :)'

