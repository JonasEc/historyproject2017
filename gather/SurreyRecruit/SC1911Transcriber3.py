#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the info from the links: RESTRICTED TO IDENTIFIED CASES!
# 2017 06 29


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
from unidecode import unidecode
from random import random
from time import sleep

######################
# Executive Decisions

## these are the [16] variables observed per person
varList = ["First name(s)","Last name","Sex", "Relationship","Marital status","Occupation","Age","Birth year","Birth place","Address","Parish","County","Country","Registration district","Registration district number","Years married","Marriage year"]
varListHH = ["First name(s)", "Last name", "Relationship", "Marital status", "Sex", "Occupation", "Age", "Birth year", "Birth place"]


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

# INPUT_SELECTOR:
name = raw_input("DataSetName")

rangeInputLower = raw_input("What lower rowlimit?")
rangeInputLower = int(rangeInputLower)
rangeInputUpper = raw_input("What upper rowlimit?")
rangeInputUpper = int(rangeInputUpper)

# setup
maxNumberHouseholdMembers = 0 

#####################
#SCRAPER

def scrapeP(datasoup):
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



def scrapeH(memberSoup,link):
	record = []

	rows = memberSoup[0].find_all("tr")

	dictList = []

	### I create a transcript specific dictionary that has as keys the table row name and as value the value for the transcript
	for column in rows[0].find_all("th"):
		variableName = column.text
		variableName = unicode(variableName) # note: we need to read it in as unicode!
		variableName = unidecode(variableName) # hence need to decode it first
		variableName = variableName.encode("ascii")	# and to be able to use it, turn it into ascii
		dictList = dictList + [variableName]
	
	for row in rows[1:]:
		cols = row.find_all("td")
		linkSoup = cols[10].a.get('href')
		personLink = "https://search.livesofthefirstworldwar.org" + linkSoup
		if personLink == link: ## I don't want to add the person of interest into the HH data-set again!
			continue
		else:
			Hdict = dict()
			for column in range(len(cols)-1):
				variableValue = cols[column].text
				variableValue = unicode(variableValue) 	
				variableValue = unidecode(variableValue) 
				variableValue = variableValue.encode("ascii")
				Hdict[dictList[column]] = variableValue
## Then I loop over household members and read their data:
			for word in varListHH:
				try:
					record = record + [Hdict[word]] ### we need to TRY and then catch the expression, in case the variable isnt recorded for the person
				except KeyError:
					record = record + [""]  ## add emtpy value if not observed

	return record, len(rows[1:])


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
linksDF = pd.read_csv(linkset, sep=',', skiprows = [i for i in (range(1,rangeInputLower) + range(rangeInputUpper+1, 17000))], header = 0)


############## LOOP THRU ALL LINKS ###########

for index, row in linksDF.iterrows():
## overhead: set up storage for this iteration etc
	if pd.isnull(row["Links"]):
		continue
	
	linkList = eval(row["Links"])
	ID = row["PersonCounter"]

	if len(linkList) > 1:
		continue
	else:
		link = linkList[0]
		HHrecord = []
		
		driver.open(link)
		sleep(random())
		datasource = driver.response().read()
		datasoup = BeautifulSoup(datasource,"lxml")	

## First: scrape detailed record for the person
		record = [ID] + scrapeP(datasoup)
## second: get less detailed record from household summary table for other members
		memberSoup = datasoup.find_all("table", class_="table table-hover tiny-table")	
## second: loop over the memebers to get their links
		if len(memberSoup) > 0:
			recordH, nHH = scrapeH(memberSoup,link)
			record = record + recordH

			maxNumberHouseholdMembers = max(maxNumberHouseholdMembers, nHH -1)

		record = record

		output.append(record)  ## add the row to the overall data set
		


########%%%%%%%%%% DONE! 

## prepare the variable names
variableNames = (["ID", "FirstName","LastName","Sex", "RelationshipWithHead","MartialStatus","Occupation","Age","BirthYear","BirthPlace",
	"Address","Parish","County","Country","RegistrationDistrict","RegistrationDistrictNumber","YearsMarried","MarriageYear"]	)


for k in range(1,maxNumberHouseholdMembers+1):
	variableNames = variableNames + (["FirstName"+str(k),"LastName"+str(k), "RelationshipWithHead"+str(k),"MartialStatus"+str(k),"Sex"+str(k), 
		"Occupation"+str(k),"Age"+str(k),"BirthYear"+str(k),"BirthPlace"+str(k)])



### now we use the panda operation data frame to turn our output list into a df
outputframe = pd.DataFrame(output, columns=variableNames)

outputFileName = outputfile + name + ".csv"
### and export that frame to a csv
outputframe.to_csv(outputFileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


## let me know when all is done
print 'done! :)' # to let me know its done 
