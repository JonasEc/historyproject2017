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
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
inputfile = ["output/SC1911/SC1911Data" + letters[k] +".csv" for k in range(len(letters))]
#inputfile = ["output/SCpeople/SCdataFinal1.csv"]


# what is our output?
outputfile = "data/SC1911Complete.csv"

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

print len(df)

important = ["ID","FirstName","LastName","Sex","RelationshipWithHead","MartialStatus","Occupation","Age","BirthYear","BirthPlace","Address","Parish","County","Country","RegistrationDistrict","RegistrationDistrictNumber","YearsMarried","MarriageYear"]
otherVarsPre = [("FirstName" + str(k) ,"LastName" + str(k), "RelationshipWithHead" +str(k) , "MartialStatus" +str(k), "Sex" + str(k),"Occupation" + str(k),"Age" +str(k), "BirthYear" + str(k),"BirthPlace" + str(k) ) for k in range(1,20)]
otherVars =  [otherVarsPre[i][j] for i in range(len(otherVarsPre)) for j in range(9)]
reordering = important + otherVars

df = df[reordering]

### save to csv
df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print 'done! :)' 