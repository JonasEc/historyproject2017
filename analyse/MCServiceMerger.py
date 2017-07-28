#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Merging Manchester Pals Service Recs
# 2017 07 24


#########################
# "administrative stuff"
import pandas as pd

from os import chdir


#########################
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# filenames
inputfilesMCS = ['output/MCServiceData' + str(i)  + '.csv' for i in range(1,5)]

outputfile = 'data/MCService.csv'


########################
# Read in the data

dfService = pd.read_csv(inputfilesMCS[0], sep =',')

for i in range(1,len(inputfilesMCS)+1):
	try:
		dfa = pd.read_csv(inputfilesMCS[i], sep =',') 
		dfService = dfService.append(dfa)
	except:
		continue


dfService = dfService.drop("Unnamed: 0", 1)

#################### FIX MAJOR BUG!!!!! COLUMNS HAVE WRONG NAMES!!!!! #############################
dfService= dfService.rename(index=str, columns={'BirthCountry':"ResidenceTown", "ResidenceCountry": "BirthCountry", "ResidenceCounty":"ResidenceCountry","ResidenceTown":"ResidenceCounty"})



dfService.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

