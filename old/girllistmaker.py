#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Girl List Maker
# 2017 05 06


#########################
# "administrative stuff"

import pandas as pd
from bs4 import BeautifulSoup
from os import chdir
import urllib2
import re
from unidecode import unidecode
from urllib2 import urlopen


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our output?
output = []
outputfile = "output/malenames1.csv"


######## THE MAIN FILE 

url = "http://www.englishboysnames.co.uk/"
listofnames = ["", "names-d-e/","names-j-to-m/","names-n-to-s/","names-t-to-z/"]

listofurls = [url + k for k in listofnames]

for page in listofurls:
	## this circumvents blocks!
	html = urllib2.Request(page, headers={'User-Agent' : "Magic Browser"}) 
	html = urlopen(html) 
	soup = BeautifulSoup(html, "lxml")
	
	for table in soup.find_all('table'):
		rows = table.find_all('tr')[1:]
		for i in range(len(rows)):
			fn = unicode(rows[i].find_all('td')[0].text) # note: we need to read it in as unicode!
			fn = unidecode(fn) # hence need to decode it first
			fn = fn.encode("ascii") # and re-encode it into ascii!
			
			output.append(fn)



outputframe = pd.DataFrame(output, columns=["Firstname"])

### and export that frame to a csv
outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

print 'done! :)' # to let me know its done 
