#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the links for SC people in 1911 Records
# 2017 05 27


#########################
# "administrative stuff"

from __future__ import division

from os import chdir
import sys
import time

from math import ceil
from random import random

import mechanize
import cookielib
from bs4 import BeautifulSoup

import pandas as pd
import re
from unidecode import unidecode


######################
# Executive Decisions

maxNumber = 1
saveper =100



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '//home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what data set are we using?
inputdata = "data/SCBaseSampleMerged.csv" 

# what is our output?
output = []

DataSetName = raw_input("What DataSetName?")
DataSetName = str(DataSetName)

outputfile = "input/SCLinks/SC1939Links/SC1939Rec" + DataSetName

outputcounter = 0
counter = 0

#######################
## The input:
# list of people we want to find (column names: 'Firstname' and 'Lastname')
rangeInputLower = raw_input("What lower rowlimit?")
rangeInputLower = int(rangeInputLower)
rangeInputUpper = raw_input("What upper rowlimit?")
rangeInputUpper = int(rangeInputUpper)

peopleDF = pd.read_csv(inputdata, sep=',', skiprows = [i for i in (range(1,rangeInputLower) + range(rangeInputUpper+1, 17000))], header = 0)



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
			driver.open(url)
			break
		except:
			time.sleep(70)
			print "had to wait for:" + url
		
	datasource = driver.response().read()
	datasoup = BeautifulSoup(datasource,"lxml")
	###### do we have a hit?
	howmany = datasoup.find_all("div", class_="SearchResultsHeader SearchResultsHeader1939")[0] 
	howmany = howmany.find_all("h3")[0]
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
				link = data_rows[i].find_all('td')[5].div.div.div.div.a.get('data-parent-record-id')
				link = "http://search.findmypast.co.uk/record?id=" + link.replace('/', '%2F') # complete the link
				# save the link to a csv to use later
				output.append(link) 
 
			return (output, False) ## hence, return captured content and DONT return continue marker
	else:
		return (False, True) ## we didnt find anything useful, hence return no content and return continue marker


##### THE ACTUAL SEARCHES

# we need to use the base search url 
baseurl = "http://search.findmypast.co.uk/results/world-Records/"
# where do we search?
recordset = "1939-register?" 
gender = "&gender=male"

# http://search.findmypast.co.uk/results/world-records/1939-register?firstname=henry&lastname=wood&yearofbirth=1896&yearofbirth_offset=1&gender=male

baseurl = baseurl + recordset

offset0 = 0
offset1 = 1
offset2 = 2

# ############## LOOP THRU ALL NAMES ##################

for index, row in peopleDF.iterrows():
	counter +=1
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

	birthyear = row["BirthYear"] # we know there is a birthyear !
	# BirthPlace
	birthplace = row["BirthPlace"]
	if birthplace and isinstance(birthplace, basestring):
		birthplace = "&keywordsplace=" + "%20".join(birthplace.split())
		birthplace = "%27".join(birthplace.split("'"))
	else:
		birthplace = ""
	birthcounty = row["BirthCounty"]		
	if birthcounty and isinstance(birthcounty, basestring):
		birthcounty = "&keywordsplace=" + "%20".join(birthplace.split()) 
		birthcounty = "%27".join(birthcounty.split("'"))
	else:
		birthcounty = ""
	attestplace = row["AttestationPlace"]
	if attestplace and isinstance(attestplace, basestring):
		attestplace = "&keywordsplace=" + "%20".join(attestplace.split())
		attestplace = "%27".join(attestplace.split("'"))
	else:
		attestplace = ""

	## ID:
	ID = row["ID"]
	Pal = row["pals"]
	Numbers = row["number"]



	if birthplace and firstname and lastname and birthyear:
		url0 = baseurl +  firstname  +  lastname  + birthplace + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0) + gender
		url1  = baseurl +  firstname  +  lastname  + birthplace + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0) + gender
	else:
		url0 = ""
		url1 = ""
	if attestplace and firstname and lastname and birthyear:
		url2  = baseurl +  firstname  +  lastname  + attestplace + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0) + gender
		url3  = baseurl +  firstname  +  lastname +  attestplace + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset1) + gender
	else:
		url2 = ""
		url3 = ""
	if birthcounty and firstname and lastname and birthyear:
		url4  = baseurl +  firstname  +  lastname  + birthcounty + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0) + gender
		url5  = baseurl +  firstname  +  lastname  + birthcounty + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset1)  + gender
	else:
		url4 = ""
		url5 = ""
	if firstname and lastname and birthyear:
		url6  = baseurl +  firstname  +  lastname + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0) + gender
		url7  = baseurl +  firstname  +  lastname +  "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset1) + gender
		url8  = baseurl +  firstname  +  lastname +  "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset2) + gender
	else:
		url6 = ""
		url7 = ""
		url8 = ""


	urllistD = [url0, url1, url2, url3, url4, url5, url6, url7, url8]

	# go to the URL, read out the file
	if maxNumber == 1:
		for url in urllistD:
			(new, cont) = searchforperson(url)
			if new:
				tempoutput = new
			if cont is False:
				break
	else:
		for url in urllistD:
			(new, cont) = searchforperson(url)
			if new:
				tempoutput = tempoutput + new
			if cont is False:
				break


	tempoutput = list(set(tempoutput))
	output.append([tempoutput, ID, Pal, Numbers]) 
		

	if counter%saveper == 0: 
		print counter
		outputfileName = outputfile + str(outputcounter) + ".csv"
		outputframe = pd.DataFrame(output, columns=["Links", "PersonCounter", "Pal", "Numbers"])
		outputframe.to_csv(outputfileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	
		output = []	
		outputcounter +=1


outputfileName = outputfile + str(outputcounter) + ".csv"
outputframe = pd.DataFrame(output, columns=["Links", "PersonCounter", "Pal", "Numbers"])
outputframe.to_csv(outputfileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


## let me know when its all done
print 'done! :)' # to let me know its done 



