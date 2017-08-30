# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 20:38:18 2017

@author: jonasmg
"""

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
palsStartDate = date(1914,7,1)

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
inputfile = "data/SCBaseSampleMerged.csv"
inputfile2 = 'input/SC1939Merged.csv'
outputfile = "data/SCBaseSampleMerged2.csv"
outputfile2 = "data/SCExtras.csv"

# Read in the data
dfSC = pd.read_csv(inputfile, sep =',')
dfLinks = pd.read_csv(inputfile2, sep =',')


#########################
# Let's restrict the sample!

## Step 1: we only care about people until end of Pal's recruitment
# first need to transform AttestationDate into useful date
dfSC.AttestationDate = pd.to_datetime(dfSC.AttestationDate).dt.date # to_datetime turns into datetime object. access the date part with dt.date 
# then we drop people who enlisted too late
dfSC = dfSC[dfSC.AttestationDate >= palsStartDate]
dfSC = dfSC.drop("Unnamed: 0", axis=1)

dfSC.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	


dfLinks = dfLinks.drop("Unnamed: 0", axis=1)

dfLinks = dfLinks.rename(index=str, columns={"PersonCounter" : "ID"})

dfNew = dfLinks.merge(dfSC, how='inner', on='ID')

dfExtras = dfNew[dfNew["Links"].isnull()]

dfExtras = dfExtras.drop(["Links"],axis=1)

### save to csv
dfExtras.to_csv(outputfile2,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print'done! :)' 

