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

## these are the variables observed per person
#varList = ["First name(s)", "Last name(s)", "DOB", "Sex" ,"Occupation", "Marital status", "Schedule", "Schedule Sub Number"]
varList = ["FirstName", "LastName", "DOB", "Sex" ,"Occupation", "MaritalStatus", "Schedule", "ScheduleSubNumber"]


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# our data input file
linkset = "input/SC1939LinkSample.csv" 

# what is our output?
output = []
outputfile = "output/SC1939data"

currentMax = 1
counter = 0

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

	table = datasoup.find_all("table", id="table-content table-hover footable default footable-loaded")[0]
	rows = table.findChildren('tr')

	for row in rows:
		cells = row.findChildren('td')
		for cell in cells[1:end]:
			variableValue = cell.text
			variableValue = unicode(variableValue) 
			variableValue = unidecode(variableValue) 
			variableValue = variableValue.encode("ascii")
			if variableValue:
				if variableValue == "Sorry, this record is officially closed.":
					continue
				else:
					record = record + [variableValue]
			else:
				record = record + [""]

	number = len(rows)

	return record, number



######################
# Mechanize Set up

#  set up the browser
driver = mechanize.Browser()

# Enable cookie support for mechanize 
cookie = pickle.load( open("cookies/cookiesFMP.pkl","rb"))

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
linksDF = pd.read_csv(linkset, sep=',', skiprows = [i for i in (range(1,rangeInputLower) + range(rangeInputUpper+1, 2000))], header = 0)


############## LOOP THRU ALL LINKS ###########

for index, row in linksDF.iterrows():
	counter = counter + 1
## overhead: set up storage for this iteration etc
	ID = row["PersonCounter"]
	link = row["Links"]	

	driver.open(link)
	sleep(random())
	datasource = driver.response().read()
	datasoup = BeautifulSoup(datasource,"lxml")	

## Scrape record for the person
	output, number = scrapeP(datasoup)
	record = [ID] + output

	if number > currentMax:
		currentMax = number
	output.append(record)  ## add the row to the overall data set
		
	variableNamesNow = ["ID"] + varList + [a + str(b) for b in range(1,currentMax) for a in varList ]
	

	if counter%25 == 0:
		outputframe = pd.DataFrame(output, columns=variableNamesNow)
		outputFileName = outputfile + name + ".csv"
		outputframe.to_csv(outputFileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

########%%%%%%%%%% DONE! 
outputframe = pd.DataFrame(output, columns=variableNamesNow)
outputFileName = outputfile + name + ".csv"
outputframe.to_csv(outputFileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


## let me know when all is done
print 'done! :)' # to let me know its done 
