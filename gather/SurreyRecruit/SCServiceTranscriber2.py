#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the info from the links: RESTRICTED TO IDENTIFIED CASES!
# 2017 07 06


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
varList = ["First name(s)","Last name","Service number", "Age", "Birth year", "Birth town", "Birth county", "Residence town", "Residence county", "Residence country", "Birth country", "Regiment", "Unit / Battalion","Year"]


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# our data input file
linkset = "input/SCServiceMerged.csv" 

# what is our output?
output = []
outputfile = "output/SCServiceData"

# INPUT_SELECTOR:
name = raw_input("DataSetName")

rangeInputLower = raw_input("What lower rowlimit?")
rangeInputLower = int(rangeInputLower)
rangeInputUpper = raw_input("What upper rowlimit?")
rangeInputUpper = int(rangeInputUpper)



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

	for link in linkList:		
		driver.open(link)
		sleep(random())
		datasource = driver.response().read()
		datasoup = BeautifulSoup(datasource,"lxml")	

## Scrape detailed record for the person
		record = [ID] + scrapeP(datasoup)

		output.append(record)  ## add the row to the overall data set
		


########%%%%%%%%%% DONE! 

## prepare the variable names
variableNames = ["ID", "FirstName","LastName","ServiceNumber", "Age", "BirthYear", "BirthTown", "BirthCounty", "BirthCountry", "ResidenceTown", "ResidenceCounty", "ResidenceCountry", "Regiment", "UnitBattalion","Year"]



### now we use the panda operation data frame to turn our output list into a df
outputframe = pd.DataFrame(output, columns=variableNames)

outputFileName = outputfile + name + ".csv"
### and export that frame to a csv
outputframe.to_csv(outputFileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


## let me know when all is done
print 'done! :)' # to let me know its done 
