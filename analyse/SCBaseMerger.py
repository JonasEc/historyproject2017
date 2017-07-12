#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# First stab at creating a useful subsample
# 2017 05 24


#########################
# "administrative stuff"

from __future__ import division

import pandas as pd
from bs4 import BeautifulSoup

from os import chdir
import re
from datetime import *
from dateutil.relativedelta import *



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfile = ["output/SCbase/SCdataFinal" + str(k) +".csv" for k in range(1,67)]
#inputfile = ["output/SCpeople/SCdataFinal1.csv"]
maxInput = len(inputfile)

# what is our output?
outputfile = "data/SCBaseComplete.csv"

# Read in the data
df = pd.read_csv(inputfile[0], sep =',')

for i in range(1,maxInput):
	try:
		dfa = pd.read_csv(inputfile[i], sep =',') 
		df = df.append(dfa)
	except:
		continue

########################
# print some sumamry stats

print len(df)


### save to csv
df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print 'done! :)' 