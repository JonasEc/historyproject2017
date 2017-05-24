#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Scraping the links for all candidates
# 2017 05 18


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


######################
# Executive Decisions

### how many records do we seek this time?
# maxNumber = 360 # this won't be exact 
#... and I can't tell why. As far as I can see, each page has 20 hits.. so we should just be dividing ceil(maxNumber/20) = page number we need.. but no!


## how often to save? 
saveThresh = 1000



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our output?
output = []
outputClass= "input/SCpeopleLinks"
csv = ".csv"

counter = 0


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

# base URL for the search: we will then loop thru "all" pages (up to max)
baseurl = "https://search.livesofthefirstworldwar.org/search/world-records/surrey-recruitment-registers-1908-1933?page="

# per save page number:
entriesPerPage =20
pagesPerSave = int(ceil(saveThresh/entriesPerPage))
totalEntries = 84672
totalSearches = int(ceil(totalEntries/saveThresh))
totalPages = int(ceil(totalEntries/entriesPerPage))


############## LOOP THRU ALL NAMES ##################


for page in range(0,totalPages+1):

# open each webpage individually
	url = baseurl + str(page)
	driver.open(url)
	datasource = driver.response().read()
	datasoup = BeautifulSoup(datasource,"lxml")

# find the table that has the entire list of search results and save all its rows
	data_rows = datasoup.find_all('tbody')[0].find_all('tr')[0:]

############ then loop over all search results on each page
	for i in range(len(data_rows)):
		dataDs = data_rows[i].find_all('td')
		# filter out wrong people:
		EventYear = dataDs[4].text
		EventYear = "".join(EventYear.split())
		EventYear = int(EventYear)
		if  EventYear >= 1914 and EventYear <= 1918:
			# get the link to the transcription
			link = dataDs[7].a.get('href')
			link = "https://search.livesofthefirstworldwar.org" + link # complete the link
			# save the link to a csv to use later
			output.append(link) 

	if page%pagesPerSave == 0:
		counter +=1
	### now we use the panda operation data frame to turn our output list into a df
		outputframe = pd.DataFrame(output, columns=["Links"])
		outputfile = outputClass + str(counter) + csv ### we need to make a new file name for each save!
	### and export that frame to a csv
		outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')
		output = [] # and clear for next save
		print page 

## let me know when its all done
print 'done! :)' # to let me know its done 



