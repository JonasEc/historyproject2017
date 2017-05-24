#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the info from the links
# 2017 05 18


#########################
# "administrative stuff"

from __future__ import division

import mechanize
import cookielib 
import urllib2
import pickle

import pandas as pd
from bs4 import BeautifulSoup

from os import chdir
import re
import time
from unidecode import unidecode


######################
# Executive Decisions

## these are the variables observed per person
varList = ["First name(s)","Last name","Service number", "Age", "Birth year", "Birth place", "Birth county", "Birth country", "Occupation", "Attestation year", "Attestation date", "Attestation place", "Unit or regiment", "Regiment", "Height", "Weight in pounds", "Eye colour", "Complexion", "Hair colour", "Chest expansion inches", "Chest size inches", "County", "Remarks", "Notes"]
rowLength = len(varList)

# choice of var names
variableNames = ["FirstName","LastName","ServiceNumber", "Age", "BirthYear", "BirthPlace", "BirthCounty", "BirthCountry", "Occupation", "AttestationYear", "AttestationDate", "AttestationPlace", "Unit", "Regiment", "Height", "Weight", "EyeColour", "Complexion", "HairColour", "ChestExpansion", "ChestSize", "County", "Remarks", "Notes"]

nSave = 1000
# how often save?





##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# our data input file
linkset = "input/SClinks/merged/SClinksMergedFinal.csv" 

# what is our output?
output = []
outputfile = ["output/SCpeople/SCdataFinal" + str(k) +".csv" for k in range(1,70)]

outputCount = -1
k = 0

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


linksDF = pd.read_csv(linkset, sep =',')
linksList = linksDF['Links'].tolist()

try:
	############## LOOP THRU ALL LINKS ###########

	for link in linksList:
		k += 1
	## overhead: set up storage for this iteration etc
		record = []

	## access the link
		try:
			driver.open(link) #if fail, wait 3min
		except:
			time.sleep(180)
			try:
				driver.open(link) # if fail, wait 5min
			except:
				time.sleep(600)
				try:
					driver.open(link) # if fail, wait 15min 
				except: 
					time.sleep(1800)
					driver.open(link)

		datasource = driver.response().read()
		datasoup = BeautifulSoup(datasource,"lxml")	

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

	 ## paste the person specific info into the dataframe
		for word in varList:
			try:
				record = record + [personDict[word]] ### we need to TRY and then catch the expression, in case the variable isnt recorded for the person
			except KeyError:
				record = record + [""]  ## add emtpy value if not observed


		output.append(record)  ## add the row to the overall data set

		if k%nSave == 0:
			outputCount +=1 
			outputframe = pd.DataFrame(output, columns=variableNames)
			outputframe.to_csv(outputfile[outputCount],sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')
			output = []

	# one last save!
	outoutCount +=1 
	outputframe = pd.DataFrame(output, columns=variableNames)
	outputframe.to_csv(outputfile[k],sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	

except:
	print k 
	print outputCount
	e = sys.exc_info()
	print e

## let me know when all is done
print 'done! :)' # to let me know its done 
