#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the links for all candidates
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
from math import ceil


######################
# Executive Decisions

# how many people are we willing to search over?
maxNumber = 100
# what age range do we want? 
minYearOfBirth = 1899 #at least 15 at outbreaj of war
maxYearOfBirth = 1864 #at most 50 at outbreak of war



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what data set are we using for our names?
namedata = "input/people.csv" 

# what is our output?
output = []
outputfile = "output/peoplelinks.csv"

# OTHER:
# To get rid of women we need a first name list
girlnames= pd.read_csv("input/femalefirstnames.csv", sep =',')
girlnames = girlnames['Firstname'].tolist()


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



######################
# THE SEARCH SET UP

# how to construct the search:
# ex: http://search.findmypast.com/results/united-kingdom-records?firstname=a&firstname_variants=true&lastname=shufflebottom&keywordsplace=manchester&datasetname=1911-census-for-england-and-wales
baseurl = "http://search.findmypast.com/results/united-kingdom-records?"

# where do we search?
recordset = "1911-census-for-england-and-wales"
place = "manchester"

# other search features:
namevar = "&firstname_variants=true"

## The input:
# list of people we want to find (column names: 'Firstname' and 'Lastname')
peopleDF = pd.read_csv(namedata, sep=',')



############## LOOP THRU ALL NAMES ##################

for index, row in peopleDF.iterrows():
######### perform the search: prepare the list of urls that we then go thru

	# read the first of people 
	firstname = row["Firstname"]
	# search engine has trouble with double first name initials
	firstname = firstname[0] 
	# read lastname of people
	lastname = row["Lastname"]

	# create the search URL
	url = baseurl + "firstname=" + firstname + namevar + "&lastname=" + lastname + "&keywordsplace=" + place + "&datasetname=" + recordset
	
	# go to the URL, read out the file
	driver.get(url)
	datasource = driver.page_source
	datasoup = BeautifulSoup(datasource,"lxml")

###### first check if we have a chance at identificaton
	howmany = datasoup.find_all("div", class_="SearchResultsHeader")[0] # this finds the number of search results
	number = re.search("[1-9][0-9]*",howmany.text)
	if number:
		number = int(number.group(0))
	else:
		continue
	if number == 0:  ## throw away people that don't exist in the data
		continue
	elif number > maxNumber: ## throw away people that are definitely unidentifiable
		continue

######## Are there several pages?
	# how many pages do we need to go thru?
	pageMax = int(ceil(number / 20)) # there are 20 people to a page 
	# create the links for all the pages
	urlList = [url + "&_page=" + str(i) for i in range(1,pageMax+1)]

####### Loop over all pages

	for page in urlList:

		## go to current page and read it out
		driver.get(page)
		datasource = driver.page_source
		datasoup = BeautifulSoup(datasource,"lxml")

		# find the table that has the entire list of search results and save all its rows
		data_rows = datasoup.find_all('tbody')[0].find_all('tr')[1:]

############ then loop over all search results on each page
		for i in range(len(data_rows)):
			# check if the person in question is of right age and gender
			fn = unicode(data_rows[i].find_all('td')[1].text) # note: we need to read it in as unicode!
			fn = unidecode(fn) # hence need to decode it first
			fn = fn.encode("ascii") # and re-encode it into ascii!
			# now we can play with the first name we read :)
			if fn == "" or len(fn) <= 2:
				continue # throw out people without names
			# to throw out women, we need to figure out if their name is possibly feamle. 
			namesplit = fn.split() #First, double names are possible
			if not set(namesplit).isdisjoint(girlnames): #then check against dictionary of names
				continue 
			if namesplit[0][0]  != firstname[0]:
				continue ## throw away people whose first name first letter does not match with the first letter we have

			yob = re.search("1[8-9][0-9][0-9]", str(data_rows[i].find_all('td')[2]) ) # get birthdate
			if yob:
				yob = int(yob.group(0)) 
			else:
				continue  # throw out without year of birth
			if yob < maxYearOfBirth or yob > minYearOfBirth:
				continue # throw out too old or too young (see EXECUTIVE DECISIONS above!)

			# get the link to the transcription
			link = data_rows[i].find_all('td')[7].a.get('href')
			link = "http://search.findmypast.com" + link # complete the link
			# save the link to a csv to use later
			output.append(link) 

	
### now we use the panda operation data frame to turn our output list into a df
outputframe = pd.DataFrame(output, columns=["Links"])

### and export that frame to a csv
outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

## close the browser when all is done
driver.quit()
print 'done! :)' # to let me know its done 



