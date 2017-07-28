#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the info from the links
# 2017 06 24


#########################
# "administrative stuff"

from __future__ import division

import mechanize
import cookielib 
import urllib2
import pickle


from os import chdir
import pandas as pd
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
from random import random
from time import sleep
import timeit

######################
# Executive Decisions

## these are the [16] variables observed per person
varList = ["First name(s)","Last name","Sex", "Relationship","Marital status","Occupation","Age","Birth year","Birth place","Address","Parish","County","Country","Registration district","Registration district number","Years married","Marriage year"]
rowLength = len(varList)



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# our data input file
linkset = "input/SC1911merged.csv" 

# what is our output?
output = []
outputfile = "output/SC1911data"

# counter
counter = 0
counterOutput =0


#####################
#SCRAPER

def scrape(datasoup):
	record = []

	individualSoup = datasoup.find_all("table", class_="table table-striped table__vertical")[0]

	personDict = dict()
	### I create a transcript specific dictionary that has as keys the table row name and as value the value for the transcript
	for row in individualSoup.find_all("tr"):
		variableName = row.find_all("th")[0].text
		variableName = unicode(variableName) # note: we need to read it in as unicode!
		variableValue = row.find_all("td")[0].text
		variableValue = unicode(variableValue) 
		variableName = unidecode(variableName) # hence need to decode it first
		variableName = variableName.encode("ascii")	# and to be able to use it, turn it into ascii
		variableValue = unidecode(variableValue) 
		variableValue = variableValue.encode("ascii")
		personDict[variableName]= variableValue

 ## this is the first couple of entries for this person's data row: person specific
	for word in varList:
		try:
			record = record + [personDict[word]] ### we need to TRY and then catch the expression, in case the variable isnt recorded for the person
		except KeyError:
			record = record + [""]  ## add emtpy value if not observed

	return record



######################
# Mechanize Set up

#  set up the browser
driver = mechanize.Browser()

# Enable cookie support for mechanize 
cookie = pickle.load( open("cookies/cookiesLFWW.pkl","rb"))

cookiejar = cookielib.LWPCookieJar() 

for s_cookie in cookie:
	try:
		cookiejar.set_cookie(cookielib.Cookie(version = 0, name = s_cookie['name'], value = s_cookie['value'], port = '80', port_specified = False, domain = s_cookie['domain'], domain_specified = True, domain_initial_dot = False, path = s_cookie['path'], path_specified = True, secure = s_cookie['secure'], expires = s_cookie['expiry'], discard = False, comment = None, comment_url = None, rest = None, rfc2109 = False))
	except KeyError:
		cookiejar.set_cookie(cookielib.Cookie(version = 0, name = s_cookie['name'], value = s_cookie['value'], port = '80', port_specified = False, domain = s_cookie['domain'], domain_specified = True, domain_initial_dot = False, path = s_cookie['path'], path_specified = True, secure = s_cookie['secure'], expires = None, discard = False, comment = None, comment_url = None, rest = None, rfc2109 = False))

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




### read in the links
linksDF = pd.read_csv(linkset, sep =',')


############## LOOP THRU ALL LINKS ###########

for index, row in linksDF.iterrows():
## overhead: set up storage for this iteration etc
	if pd.isnull(row["Links"]):
		continue
	
	linkList = eval(row["Links"])
	ID = row["PersonCounter"]

	for link in linkList:
		personLinkList = []
		
		driver.open(link)
		sleep(random())
		datasource = driver.response().read()
		datasoup = BeautifulSoup(datasource,"lxml")	

## first: get the household summary table
		memberSoup = datasoup.find_all("table", class_="table table-hover tiny-table")	
## second: loop over the memebers to get their links
		if len(memberSoup) > 0:
			for row in memberSoup[0].find_all("tr")[1:]:
				linkSoup = row.find_all("td")[10].a.get('href')
				personLink = "https://search.livesofthefirstworldwar.org" + linkSoup
				if personLink == link: ## I don't want to add the person of interest into the link-set again!
					continue
				else:
					personLinkList.append(personLink)

		record = scrape(datasoup)

	## next we add all the other household numbers to the row!

		if len(personLinkList) > 0:
			for linkM in personLinkList:
				driver.open(linkM)
				sleep(random())
				datasource = driver.response().read()
				datasoup = BeautifulSoup(datasource,"lxml")	
				recordM = scrape(datasoup)
				record = record + recordM 

		record = record + [ID]
		output.append(record)  ## add the row to the overall data set
		print len(output)
		print output
		
	if len(output) % 25 == 0 and len(output) > 0:
		print "saving..."
		counterOutput += 1
		## calculate how many people there are at most in a row
		maxRowLength = len(max(output,key=len))
		maxNumberHouseholdMembers = int(maxRowLength/rowLength)

		## prepare the variable names
		variableNames = (["FirstName","LastName","Sex", "RelationshipWithHead","MartialStatus","Occupation","Age","BirthYear","BirthPlace",
			"Address","Parish","Country","Country","RegistrationDistrict","RegistrationDistrictNumber","YearsMarried","MarriageYear"]	)

		for k in range(1,maxNumberHouseholdMembers):
			variableNames = variableNames + (["FirstName"+str(k),"LastName"+str(k),"Sex"+str(k), "RelationshipWithHead"+str(k),"MartialStatus"+str(k),
				"Occupation"+str(k),"Age"+str(k),"BirthYear"+str(k),"BirthPlace"+str(k),"Address"+str(k),"Parish"+str(k),"Country"+str(k),
				"Country"+str(k),"RegistrationDistrict"+str(k),"RegistrationDistrictNumber"+str(k),"YearsMarried"+str(k),"MarriageYear"+str(k)]	)

		variableNames = variableNames + ["ID"]

		### now we use the panda operation data frame to turn our output list into a df
		outputframe = pd.DataFrame(output, columns=variableNames)

		outputFileName = outputfile + str(counterOutput) + ".csv"
		### and export that frame to a csv
		outputframe.to_csv(outputFileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


########%%%%%%%%%% DONE! 

maxRowLength = len(max(output,key=len))
maxNumberHouseholdMembers = int(maxRowLength/rowLength)

## prepare the variable names
variableNames = (["FirstName","LastName","Sex", "RelationshipWithHead","MartialStatus","Occupation","Age","BirthYear","BirthPlace",
	"Address","Parish","Country","Country","RegistrationDistrict","RegistrationDistrictNumber","YearsMarried","MarriageYear"]	)

for k in range(1,maxNumberHouseholdMembers):
	variableNames = variableNames + (["FirstName"+str(k),"LastName"+str(k),"Sex"+str(k), "RelationshipWithHead"+str(k),"MartialStatus"+str(k),
		"Occupation"+str(k),"Age"+str(k),"BirthYear"+str(k),"BirthPlace"+str(k),"Address"+str(k),"Parish"+str(k),"Country"+str(k),
		"Country"+str(k),"RegistrationDistrict"+str(k),"RegistrationDistrictNumber"+str(k),"YearsMarried"+str(k),"MarriageYear"+str(k)]	)

variableNames = variableNames + ["ID"]

### now we use the panda operation data frame to turn our output list into a df
outputframe = pd.DataFrame(output, columns=variableNames)

outputFileName = outputfile + "FINAL" + ".csv"
### and export that frame to a csv
outputframe.to_csv(outputFileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


## let me know when all is done
print 'done! :)' # to let me know its done 
