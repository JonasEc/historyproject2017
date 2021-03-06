#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the info from the links
# 2017 05 06


#########################
# "administrative stuff"

from __future__ import division

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
from os import chdir
import re
from unidecode import unidecode
import time


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
linkset = "output/peoplelinks.csv" 

# what is our output?
output = []
outputfile = "output/peopledata.csv"

# counter
counter = 0


######################
# Selenium Set up

## log into findmypast.com
driver = webdriver.Chrome()
driver.get('https://www.findmypast.com/sign-in')

username = driver.find_element_by_id("emailAddress")
password = driver.find_element_by_id("password")

username.send_keys("jonas.muellergastell@gmail.com")
password.send_keys("History2017!")

driver.find_element_by_name("submit").click()


time.sleep(15)



### read in the links
linksDF = pd.read_csv(linkset, sep =',')
linksList = linksDF['Links'].tolist()



############## LOOP THRU ALL LINKS ###########

for link in linksList:

## overhead: set up storage for this iteration etc
	personLinkList = []
	record = []

## access the link
	driver.get(link)
	datasource = driver.page_source
	datasoup = BeautifulSoup(datasource,"lxml")	

## first: get the household summary table
	memberSoup = datasoup.find_all("table", class_="table table-hover tiny-table")	
## second: loop over the memebers to get their links
	if len(memberSoup) > 0:
		for row in memberSoup[0].find_all("tr")[1:]:
			linkSoup = row.find_all("td")[9].a.get('href')
			personLink = "http://search.findmypast.com" + linkSoup
			if personLink == link: ## I don't want to add the person of interest into the link-set again!
				continue
			else:
				personLinkList.append(personLink)

## next: start the data set! 
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

	if personDict["Sex"] == "Female":
		print "Throw out" + personDict['First name(s)'] + " " + personDict['Last name'] + " because female"
		counter += 1
		print counter
		continue ##<<< throw out any women

 ## this is the first couple of entries for this person's data row: person specific
	for word in varList:
		try:
			record = record + [personDict[word]] ### we need to TRY and then catch the expression, in case the variable isnt recorded for the person
		except KeyError:
			record = record + [""]  ## add emtpy value if not observed

## next we add all the other household numbers to the row!
	for person in personLinkList:
		driver.get(person)
		datasource = driver.page_source
		datasoup = BeautifulSoup(datasource,"lxml")	
		individualSoup = datasoup.find_all("table", class_="table table-striped table__vertical")[0]

		personDict = dict()
		for row in individualSoup.find_all("tr"):
			variableName = row.find_all("th")[0].text
			variableName = unicode(variableName) 
			variableValue = row.find_all("td")[0].text
			variableValue = unicode(variableValue) 
			variableName = unidecode(variableName)
			variableName = variableName.encode("ascii")
			variableValue = unidecode(variableValue) 
			variableValue = variableValue.encode("ascii")
			personDict[variableName]= variableValue

### this is the household specific vars for the person
		for word in varList:
			try:
				record = record + [personDict[word]]
			except KeyError:
				record = record + [""] 
		

	output.append(record)  ## add the row to the overall data set

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

### now we use the panda operation data frame to turn our output list into a df
outputframe = pd.DataFrame(output, columns=variableNames)

### and export that frame to a csv
outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

## close the browser when all is done
driver.quit()
print 'done! :)' # to let me know its done 
