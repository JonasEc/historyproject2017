#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Girl List Maker Vol2
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
outputfile = "output/malenames2.csv"


whitelist = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

######## THE MAIN FILE 

for country in ["irish", "english"]:

	url = "http://www.20000-names.com/male_" + country + "_names"
	if country == "english":
		listofnames = [""] + ["_0" + str(k) for k in range(2,10)] + ["_" + str(k) for k in range(10,18)]
	else:
		listofnames = ["", "_02"]

	listofurls = [url + k  +".htm" for k in listofnames]

	for page in listofurls:
		## this circumvents blocks!
		html = urllib2.Request(page, headers={'User-Agent' : "Magic Browser"}) 
		html = urlopen(html) 
		soup = BeautifulSoup(html, "lxml")
		
		table = soup.find_all('ol')[0]
		rows = table.find_all('b')
		for i in range(len(rows)):
			try:
				fn = unicode(rows[i].a.get('name')) # note: we need to read it in as unicode!
			except AttributeError:
				fn = unicode(rows[i].text)
			fn = unidecode(fn) # hence need to decode it first
			fn = fn.encode("ascii") # and re-encode it into ascii!
			fn.replace('"',"")
			fn.replace("'","")
			fn.replace(" ", "")
			fn.rstrip()
			fn = ''.join(filter(whitelist.__contains__, fn))
			fn = fn[0] + fn[1:].lower()
			output.append(fn)



outputframe = pd.DataFrame(output, columns=["Firstname"])

### and export that frame to a csv
outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

print 'done! :)' # to let me know its done 
