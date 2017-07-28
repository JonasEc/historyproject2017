#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the links for MC people in 1911 Records
# 2017 05 27


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
from random import random
import sys
import time


######################
# Executive Decisions

maxNumber = 1

##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what data set are we using?
inputdata1 = "data/MCPComplete.csv" 
inputdata2 = "output/MCServiceForScrape.csv" 

# what is our output?
output = []

DataSetName = raw_input("What DataSetName?")
DataSetName = str(DataSetName)

outputfile = "input/MClinks/MC1911Links/MC1911set" + DataSetName


##### THE ACTUAL SEARCHES

# we need to use the base search url 
baseurl = "https://search.livesofthefirstworldwar.org/search/world-records/"
# where do we search?
recordset = "1911-census-for-england-and-wales?" 

baseurl = baseurl + recordset

## The input:
SearchType = int(raw_input("SearchType?"))

if SearchType ==1:
	# list of people we want to find (column names: 'Firstname' and 'Lastname')
	rangeInputLower = raw_input("What lower rowlimit?")
	rangeInputLower = int(rangeInputLower)
	rangeInputUpper = raw_input("What upper rowlimit?")
	rangeInputUpper = int(rangeInputUpper)
	peopleDF = pd.read_csv(inputdata1, sep=',', skiprows = [i for i in (range(1,rangeInputLower) + range(rangeInputUpper+1, 17000))], header = 0)
else:
	peopleDF = pd.read_csv(inputdata2, sep=',')

#### 
parish1 = "&parish=south%20manchester"
parish2="&parish=north%20manchester"
parish3 = "&parish=manchester"
county = "&county=lancashire"


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


### searching function:
# this function takes a url, tries to read out the links, and then either returns a link or "False" (ie no content) 
# +  a continuation marker ("TRUE = continue", "FALSE = dont continue")
def searchforperson(url):
	output = []

	time.sleep(random()) 

	if url == "": ## if url is actually empty, return no content and continue to next iteration
		return (False, True)

	while True:
		try:
			driver.open(url) #if fail, wait 90 sec (on average)
			break
		except:
			time.sleep(180*random())

	datasource = driver.response().read()
	datasoup = BeautifulSoup(datasource,"lxml")
	###### do we have a hit?
	howmany = datasoup.find_all("div", class_="SearchResultsHeader")[0] # this finds the number of search results
	number =  [int(s) for s in howmany.text.split() if s.isdigit()]
	if number: ## are there any numbers?
		if number[0] == 0:  # we need to try a less restrictive search! 
			return (False, True) ## hence, return no content and return continue marker
		elif number[0] > maxNumber: ## throw away people that are unidentifiable
			return (False, False) ## hence, return no content and DONT return continue marker
		else:
			# find the table that has the entire list of search results and save all its rows
			data_rows = datasoup.find_all('tbody')[0].find_all('tr')
			# get the link to the transcription
			for i in range(len(data_rows)):
				link = data_rows[i].find_all('td')[7].a.get('href')
				link = "https://search.livesofthefirstworldwar.org" + link # complete the link
				# save the link to a csv to use later
				output.append(link) 
 
			return (output, False) ## hence, return captured content and DONT return continue marker
	else:
		return (False, True) ## we didnt find anything useful, hence return no content and return continue marker




############## LOOP THRU ALL NAMES ##################

for index, row in peopleDF.iterrows():
	tempoutput = []
######### perform the search: prepare the list of urls that we then go thru

	# read the first of people 
	firstname = row["FirstName"]
	if firstname and isinstance(firstname, basestring):
		firstname = "firstname=" + "%20".join(firstname.split())
		firstname = "%27".join(firstname.split("'"))
	else:
		firstname = ""
	# read lastname of people
	lastname = row["LastName"] 
	if lastname and isinstance(lastname, basestring):
		lastname = "&lastname=" + "%20".join(lastname.split())
		lastname = "%27".join(lastname.split("'"))
	else:
		lastname = ""

	
	## ID:
	ID = row["ID"]

	if SearchType ==1:

		url1 = baseurl + firstname + lastname + parish1
		url2 = baseurl + firstname + lastname + parish2
		url3 = baseurl + firstname + lastname + parish3
		url4 = baseurl + firstname + lastname + county

		urllistD = [url1, url2, url3, url4]

	else:
		BirthYear = row["BirthYear"]
		if BirthYear and isinstance(BirthYear, basestring):
			BirthYear = "firstname=" + "%20".join(BirthYear.split())
			BirthYear = "%27".join(BirthYear.split("'"))
			BirthYear = '&yearofbirth=' + BirthYear + '&yearofbirth_offset=2'
		else:
			BirthYear = ""
		# read birthtown of people
		BirthTown = row["BirthTown"] 
		if BirthTown and isinstance(BirthTown, basestring):
			BirthTown = "&lastname=" + "%20".join(BirthTown.split())
			BirthTown = "%27".join(BirthTown.split("'"))
			BirthTown = '&whereborntext=' + BirthTown 
		else:
			BirthTown = ""
		BirthCounty = row["BirthCounty"] 
		if BirthCounty and isinstance(BirthCounty, basestring):
			BirthCounty = "&lastname=" + "%20".join(BirthCounty.split())
			BirthCounty = "%27".join(BirthCounty.split("'"))
			BirthCounty = '&whereborntext=' + BirthCounty 
		else:
			BirthCounty = ""
		ResidenceTown = row["ResidenceTown"] 
		if ResidenceTown and isinstance(ResidenceTown, basestring):
			ResidenceTown = "&lastname=" + "%20".join(ResidenceTown.split())
			ResidenceTown = "%27".join(ResidenceTown.split("'"))
			ResidenceTown = '&keywordsplace=' + ResidenceTown 
		else:
			ResidenceTown = ""
		ResidenceCounty = row["BirthCounty"] 
		if ResidenceCounty and isinstance(ResidenceCounty, basestring):
			ResidenceCounty = "&lastname=" + "%20".join(ResidenceCounty.split())
			ResidenceCounty = "%27".join(ResidenceCounty.split("'"))
			ResidenceCounty = '&keywordsplace=' + ResidenceCounty 
		else:
			ResidenceCounty = ""

		url1 = baseurl + firstname + lastname + BirthTown + BirthYear
		url2 = baseurl + firstname + lastname + BirthTown
		url3 = baseurl + firstname + lastname + BirthCounty + BirthYear
		url4 = baseurl + firstname + lastname + ResidenceTown + BirthYear
		url5 = baseurl + firstname + lastname + ResidenceTown
		url6 = baseurl + firstname + lastname + ResidenceCounty + BirthYear	

		urllistD = [url1, url2, url3, url4, url5, url6]	


	# go to the URL, read out the file

	for url in urllistD:
		(new, cont) = searchforperson(url)
		if new:
			tempoutput = tempoutput + new
		if cont is False:
			break


	tempoutput = list(set(tempoutput))
	output.append([tempoutput, ID]) 
		




outputfileName = outputfile + ".csv"
outputframe = pd.DataFrame(output, columns=["Links", "PersonCounter"])
outputframe.to_csv(outputfileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


## let me know when its all done
print 'done! :)' # to let me know its done 



