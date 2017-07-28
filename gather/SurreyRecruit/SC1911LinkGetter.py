#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the links for SC people in 1911 Records
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

maxNumber = 20
saveper =100



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what data set are we using?
inputdata = "data/SCsample2.csv" 

# what is our output?
output = []

DataSetName = raw_input("What DataSetName?")
DataSetName = str(DataSetName)

outputfile = "input/SC1911Links/SC1911Rec" + DataSetName

outputcounter = 0

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

	try:
		driver.open(url)
	except:
		time.sleep(70)
		try:
			driver.open(url)
		except:
			e = sys.exc_info()
			print e
			print url 
			return (False, True)

	datasource = driver.response().read()
	datasoup = BeautifulSoup(datasource,"lxml")
	###### do we have a hit?
	howmany = datasoup.find_all("div", class_="SearchResultsHeader")[0] # this finds the number of search results
	number =  [int(s) for s in howmany.text.split() if s.isdigit()]
	if number: ## are there any numbers?
		if number[0] == 0:  # we need to try a less restrictive search! 
			return (False, True) ## hence, return no content and return contunue marker
		elif number[0] > maxNumber: ## throw away people that are unidentifiable
			return (False, False) ## hence, return no content and DONT return contunue marker
		else:
			# find the table that has the entire list of search results and save all its rows
			data_rows = datasoup.find_all('tbody')[0].find_all('tr')
			# get the link to the transcription
			for i in range(len(data_rows)):
				link = data_rows[i].find_all('td')[7].a.get('href')
				link = "https://search.livesofthefirstworldwar.org" + link # complete the link
				# save the link to a csv to use later
				output.append(link) 
 
			return (output, False) ## hence, return captured content and DONT return contunue marker
	else:
		return (False, True) ## we didnt find anything useful, hence return no content and return contunue marker


##### THE ACTUAL SEARCHES

# we need to use the base search url 
baseurl = "https://search.livesofthefirstworldwar.org/search/world-records/"
# where do we search?
recordset = "1911-census-for-england-and-wales?" 

born = "&SearchFacets[0].FriendlyId=WherebornText&SearchFacets[0].Value="
bornVariant = "&SearchFacets[0].Variants=true"

baseurl = baseurl + recordset

## The input:
# list of people we want to find (column names: 'Firstname' and 'Lastname')
rangeInputLower = raw_input("What lower rowlimit?")
rangeInputLower = int(rangeInputLower)
rangeInputUpper = raw_input("What upper rowlimit?")
rangeInputUpper = int(rangeInputUpper)

peopleDF = pd.read_csv(inputdata, sep=',', skiprows = [i for i in (range(1,rangeInputLower) + range(rangeInputUpper+1, 17000))], header = 0)


## Var Names:
## FirstName,LastName,ServiceNumber,Age,BirthYear,BirthPlace,BirthCounty,BirthCountry,
## Occupation,AttestationYear,AttestationDate,AttestationPlace,Unit,Regiment,Height,Weight,
## EyeColour,Complexion,HairColour,ChestExpansion,ChestSize,County,Remarks,Notes,Type,AgeYears,AgeMonths,BirthDate,AgeAtCutoff

offset0 = 0
offset1 = 1
offset2 = 2
counter = 1

############## LOOP THRU ALL NAMES ##################

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
	# ServiceNumber
	# servicenumber = row["ServiceNumber"]
	# if servicenumber and servicenumber is not "-":
	# 	servicenumber= "&servicenumber==" + servicenumber
	# BirthYear
	birthyear = row["BirthYear"] # we know there is a birthyear !
	# BirthPlace
	birthplace = row["BirthPlace"]
	if birthplace and isinstance(birthplace, basestring):
		birthplace = born + "%20".join(birthplace.split())
		birthplace = "%27".join(birthplace.split("'"))
	else:
		birthplace = ""
	birthcounty = row["BirthCounty"]		
	if birthcounty and isinstance(birthcounty, basestring):
		birthcounty = born + "%20".join(birthplace.split()) 
		birthcounty = "%27".join(birthcounty.split("'"))
	else:
		birthcounty = ""
	# AttestationPlace
	attestplace = row["AttestationPlace"]
	if attestplace and isinstance(attestplace, basestring):
		attestplace = "&keywordsplace=" + "%20".join(attestplace.split())
		attestplace = "%27".join(attestplace.split("'"))
	else:
		attestplace = ""

	## ID:
	ID = row["ID"]


	# Regiment
	# regiment = row["Regiment"]
	# if regiment and isinstance(regiment, basestring):
	# 	regiment = "&regiment=" + "%20".join(regiment.split())
	# 	regiment = "&regiment=" + "%27".join(regiment.split("'"))
	# else:
	# 	regiment = ""

	# create the search URLs (decreasingly specific)



	if birthplace and firstname and lastname and birthyear:
		url00 = baseurl +  firstname  +  lastname  + birthplace + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0)
		url0  = baseurl +  firstname  +  lastname  + birthplace + bornVariant + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0)	
		url1  = baseurl +  firstname  +  lastname  + birthplace + bornVariant + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset1) 
	else:
		url00 = ""
		url0 = ""
		url1 = ""
	if attestplace and firstname and lastname and birthyear:
		url2  = baseurl +  firstname  +  lastname  + attestplace + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0) 
		url3  = baseurl +  firstname  +  lastname +  attestplace + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset1) 
	else:
		url2 = ""
		url3 = ""
	if birthcounty and firstname and lastname and birthyear:
		url40 = baseurl +  firstname  +  lastname  + birthcounty + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0)
		url4  = baseurl +  firstname  +  lastname  + birthcounty + bornVariant + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0)
		url5  = baseurl +  firstname  +  lastname  + birthcounty + bornVariant + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset1) 
	else:
		url40 = ""
		url4 = ""
		url5 = ""
	if firstname and lastname and birthyear:
		url6  = baseurl +  firstname  +  lastname + "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset0) 
		url7  = baseurl +  firstname  +  lastname +  "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset1) 
		url8  = baseurl +  firstname  +  lastname +  "&yearofbirth=" + str(birthyear) + "&yearofbirth_offset=" + str(offset2) 
	else:
		url6 = ""
		url7 = ""
		url8 = ""


	urllistD = [url00, url0, url1, url2, url3, url40, url4, url5, url6, url7, url8]

	# go to the URL, read out the file

	for url in urllistD:
		(new, cont) = searchforperson(url)
		if new:
			tempoutput = tempoutput + new
		if cont is False:
			break


	tempoutput = list(set(tempoutput))
	output.append([tempoutput, ID]) 
		

	if counter%saveper == 0: 
		print counter
		outputfileName = outputfile + str(outputcounter) + ".csv"
		outputframe = pd.DataFrame(output, columns=["Links", "PersonCounter"])
		outputframe.to_csv(outputfileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	
		output = []	
		outputcounter +=1


outputfileName = outputfile + str(outputcounter) + ".csv"
outputframe = pd.DataFrame(output, columns=["Links", "PersonCounter"])
outputframe.to_csv(outputfileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


## let me know when its all done
print 'done! :)' # to let me know its done 



