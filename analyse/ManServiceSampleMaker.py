#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# First stab at creating a useful subsample ManNonPals
# 2017 07 25


#########################
# "administrative stuff"

import pandas as pd

from os import chdir
import re



########################
# Exec Decisions

# End of Pals Recruitment:
palsEndDate = 1916 ## year month day 
ageCutoff = 19
BirthYearCutOff = palsEndDate - ageCutoff

# types of regiments:


#####################
# Aide Memoires:

# variableNames = ["ID", "FirstName","LastName","ServiceNumber", "Age", "BirthYear", "BirthTown", "BirthCounty", "BirthCountry", "ResidenceTown", "ResidenceCounty", "ResidenceCountry", "Regiment", "UnitBattalion","Year"]

#####++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++################


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfilesMCS = ["output/ManNonPalsServiceData" + str(k) + ".csv" for k in range(5)]
batList = 'data/ManBattListTyped.csv'

# what is our output?
outputfile = "data/ManServiceSample.csv"
listfileName = 'output/ManBattList.csv'

# Read in the data
dfService = pd.read_csv(inputfilesMCS[0], sep =',')

for i in range(1,len(inputfilesMCS)+1):
	try:
		dfa = pd.read_csv(inputfilesMCS[i], sep =',') 
		dfService = dfService.append(dfa)
	except:
		continue

dfService.to_csv("data/ManServiceComplete.csv",sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

######################## GET ALL BATTALION NAMES ###################
# listOfBattalions = dfService["UnitBattalion"].tolist()
# setOfBattalions = set(listOfBattalions)
# listOfBattalions = list(setOfBattalions)

#dfList = dfService.groupby('UnitBattalion')['ID'].nunique()
#dfList.to_csv(listfileName,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')



dfService = dfService.drop('Unnamed: 0', 1)
dfService = dfService.drop('ID', 1)

dfService.drop_duplicates(inplace=True)

print('Total Sample: ' + str(len(dfService)))

#################### FIX MAJOR BUG!!!!! COLUMNS HAVE WRONG NAMES!!!!! #############################
dfService= dfService.rename(index=str, columns={'BirthCountry':"ResidenceTown", "ResidenceCountry": "BirthCountry", "ResidenceCounty":"ResidenceCountry","ResidenceTown":"ResidenceCounty"})


#########################
# Let's restrict the sample!

## Step 1: we only care about people during Pal's recruitment
## HOW TO DO THIS STEP? IT IS NOT CLEAR WHAT THE YEAR REALLY CORRESPONDS TO .. CHECK IN THE PRINTED IMAGES!
dfService["Year"] = pd.to_numeric(dfService["Year"], errors='coerce')
dfService = dfService.dropna(axis=0,subset=["Year"],how='any')
dfService = dfService.loc[(dfService["Year"] >= 1914) & (dfService["Year"] <= 1918)]
print('Correct Years only: ' + str(len(dfService)))

## Step 2: kick out people who are too young to serve (?)
dfService["BirthYear"] = pd.to_numeric(dfService["BirthYear"], errors='coerce')
dfService = dfService.dropna(axis=0,subset=["BirthYear"],how='any')
dfService = dfService[dfService["BirthYear"] < BirthYearCutOff]
print('No one too young: ' + str(len(dfService)))

## Step 3: kick out people with missing data
dfService = dfService.dropna(axis=0,subset=["UnitBattalion", 'FirstName'],how='any')
dfService = dfService.dropna(axis=0,subset=["BirthTown", 'BirthCounty',"ResidenceTown", 'ResidenceCounty'],thresh=3)
print('After missing Data: ' + str(len(dfService)))

## Step 4: We only want to include NON PALS and NON TERRITORIAL and NON PREWAR ENLISTED BATTALIONS:
# here is a list of battalions by type:
dfBatType = pd.read_csv(batList,sep=',')
# merge:
dfService = pd.merge(dfService, dfBatType, how= "inner" , on= "UnitBattalion")

dfService = dfService.loc[(dfService['Type'] == "New Armies") | (dfService['Type'] == "Pal")]
print('Only Pals and New Armies: ' + str(len(dfService)))
dfService = dfService[dfService["Reserve"] == 0]
print('Only Non Reserve: ' + str(len(dfService)))

dfService['ID'] = dfService.index
howMany = dfService.groupby('Type')['ID'].nunique()


dfService.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	
## let me know when all is done
print('done! :)') 
