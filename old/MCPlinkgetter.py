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
maxNumber = 360 # this won't be exact 
#... and I can't tell why. As far as I can see, each page has 20 hits.. so we should just be dividing ceil(maxNumber/20) = page number we need.. but no!



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our output?
output = []
outputfile = "input/MCPlinks.csv"



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
baseurl = "http://search.findmypast.com/results/united-kingdom-records?datasetname=manchester-regiment-city-battalions-1914-1916&_page="

# max page number:
entriesPerPage =20
maxPage = int(ceil(maxNumber/entriesPerPage))


############## LOOP THRU ALL NAMES ##################

for page in range(1,maxPage+1):

# open each webpage individually
	url = baseurl + str(page)
	driver.open(url)
	datasource = driver.response().read()
	datasoup = BeautifulSoup(datasource,"lxml")

# find the table that has the entire list of search results and save all its rows
	data_rows = datasoup.find_all('tbody')[0].find_all('tr')[1:]

############ then loop over all search results on each page
	for i in range(len(data_rows)):
		# get the link to the transcription
		link = data_rows[i].find_all('td')[7].a.get('href')
		link = "http://search.findmypast.com" + link # complete the link
		# save the link to a csv to use later
		output.append(link) 

	
### now we use the panda operation data frame to turn our output list into a df
outputframe = pd.DataFrame(output, columns=["Links"])

### and export that frame to a csv
outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')


## let me know when its all done
print 'done! :)' # to let me know its done 



