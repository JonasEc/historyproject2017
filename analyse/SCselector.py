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
import datetime


########################
# Exec Decisions

# End of Pals Recruitment:
palsEndDate = datetime.date(1916,3,2) ## year month day 
ageCutOff = 18


# types of regiments:


#####################
# Aide Memoires:

# variableNames = ["FirstName","LastName","ServiceNumber", "Age", "BirthYear", "BirthPlace", "BirthCounty", "BirthCountry", "Occupation", "AttestationYear", "AttestationDate", "AttestationPlace", "Unit", "Regiment", "Height", "Weight", "EyeColour", "Complexion", "HairColour", "ChestExpansion", "ChestSize", "County", "Remarks", "Notes"]

#####++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++################


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfile = ["output/SCpeople/SCdataFinal" + str(k) +".csv" for k in range(1,67)]
#inputfile = ["output/SCpeople/SCdataFinal1.csv"]
maxInput = len(inputfile)
listFile = "output/listofregimentsTypedManualV1.csv"

# what is our output?
outputfile = "data/SCsample.csv"

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


#########################
# Let's restrict the sample!

## Step 1: we only care about people until end of Pal's recruitment
# first need to transform AttestationDate into useful date
df.AttestationDate = pd.to_datetime(df.AttestationDate)
# then we drop people who enlisted too late
df = df[df.AttestationDate <= palsEndDate]

## Step 2: we want infantry only:
# first, I turn "Regiment" into a categorical variable
df["Regiment"] = df["Regiment"].astype('category')
df["Unit"] = df["Unit"].astype('category')
# second, I export the list of all unique values
# listofregiments = df.Regiment.cat.categories.tolist()
# exportList1 = pd.DataFrame(listofregiments, columns=["Regiment"])

# third we need to turn add types to this (outside program/ by hand)

# # fourth, I read these lists back into pandas
dfList = pd.read_csv(listFile, sep =',') 

df = pd.merge(df, dfList, how= "inner" , on= "Regiment")

# # and kick out non-infantry:
df = df[df.Type == 0]



## Step 3: kick out people who are too young to serve (?)
# first need to clean up age variable:
def ageCleanerYears(x):
	years = re.search("([0-9][0-9]) [Yy]ears",x)
	if years:
		return years.group(1)
	else:
		return "999"
def ageCleanerMonths(x):
	months = re.search("([0-9][0-9]?) [Mm]onths",x)
	if months:
		return months.group(1)
	else:
		return "999"

df["AgeYears"] = df["Age"].apply(ageCleanerYears).astype(int) 
df["AgeMonths"] = df["Age"].apply(ageCleanerMonths).astype(int) 
# intermediate step: do we keep people without age in?
dfNoAge = df[df["AgeYears"] == 999]
df = df[df["AgeYears"] != 999]
# second, kick out people below 18:
df = df[df["AgeYears"] >= 18]


print len(df)


### save to csv
df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print 'done! :)' 
