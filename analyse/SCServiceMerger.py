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

from os import chdir
import re
from datetime import *
from dateutil.relativedelta import *




##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our input?
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
inputfile = ["output/SCService/SCServiceData" + letters[k] +".csv" for k in range(len(letters))]
#inputfile = ["output/SCpeople/SCdataFinal1.csv"]


# what is our output?
outputfile = "data/SCServiceComplete.csv"

# Read in the data
df = pd.read_csv(inputfile[0], sep =',')

for i in range(1,len(inputfile)+1):
	try:
		dfa = pd.read_csv(inputfile[i], sep =',') 
		df = df.append(dfa)
	except:
		continue

########################
# print some sumamry stats

print(len(df))

df= df.rename(index=str, columns={'BirthCountry':"ResidenceTown", "ResidenceCountry": "BirthCountry", "ResidenceCounty":"ResidenceCountry","ResidenceTown":"ResidenceCounty"})

df = df.drop(["Unnamed: 0"], 1)

### save to csv
df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print( 'done! :)' )



