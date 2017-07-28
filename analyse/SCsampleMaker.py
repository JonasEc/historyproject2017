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


########################
# Exec Decisions

# End of Pals Recruitment:
palsEndDate = date(1916,3,2) ## year month day 
ageCutoff = 19


# types of regiments:


#####################
# Aide Memoires:

# variableNames = ["FirstName","LastName","ServiceNumber", "Age", "BirthYear", "BirthPlace", "BirthCounty", "BirthCountry", "Occupation", "AttestationYear", "AttestationDate", "AttestationPlace", "Unit", "Regiment", "Height", "Weight", "EyeColour", "Complexion", "HairColour", "ChestExpansion", "ChestSize", "County", "Remarks", "Notes"]

#####++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++################


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfile = "data/SCBaseComplete.csv"
listFile = "data/listofregimentsTypedManualV1.csv"

# what is our output?
outputfile = "data/SCBaseSample2.csv"

# Read in the data
df = pd.read_csv(inputfile, sep =',')



#########################
# Let's restrict the sample!

## Step 1: we only care about people until end of Pal's recruitment
# first need to transform AttestationDate into useful date
df.AttestationDate = pd.to_datetime(df.AttestationDate).dt.date # to_datetime turns into datetime object. access the date part with dt.date 
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
dfList = pd.read_csv(listFile, sep =',', skipinitialspace=True, usecols=["Regiment", "Type"]) 

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
def birthday(row):
	row["BirthDate"] = row["AttestationDate"] - relativedelta(months = row["AgeMonths"],years = row["AgeYears"])
#	row["BirthDate"] = pd.to_datetime(row["BirthDate"])
	return row["BirthDate"]
def ageatcutoff(row):
	timedelta = palsEndDate- row["BirthDate"] # get a timedelta object in days between palsenddate and the birthdate of the person
	timedelta = int(timedelta.days)/365.25 # access the days element and turn into integer, then divide by 365.25
	row["AgeAtCutoff"] = timedelta
	return row["AgeAtCutoff"] 


df["AgeYears"] = df["Age"].apply(ageCleanerYears).astype(int) 
df["AgeMonths"] = df["Age"].apply(ageCleanerMonths).astype(int) 
# intermediate step: do we keep people without age in?
dfNoAge = df[df["AgeYears"] == 999]
df = df[df["AgeYears"] != 999]
df = df[df["BirthYear"] != ""]
df["BirthYear"] = df["BirthYear"].astype(int)
# second, kick out people below cutoff age at at cutoff date:
df["BirthDate"] = df.apply(birthday, axis = 1)
df["AgeAtCutoff"] = df.apply(ageatcutoff, axis = 1)

df = df[df["AgeAtCutoff"] >= ageCutoff]



df.drop(df.columns[0], axis=1, inplace=True)

length = len(df)


IDlist = [i for i in range(length)]

IDcol = pd.Series(IDlist,index=df.index)

df["ID"] = IDcol


### save to csv
df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print('done! :)') 

