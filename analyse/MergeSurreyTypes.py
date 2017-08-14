#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Create Battalion Types SC
# 2017 07 27


#########################
# "administrative stuff"

import pandas as pd

from os import chdir



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfileSC = 'data/SCBaseSample2.csv'
listfile = 'data/SCBattsTypes.csv'

#and output?
outputfile = 'data/SCBaseSampleMerged.csv'

# Read in the data
dfSurreyTypes = pd.read_csv(listfile,sep =',')
dfSurreyTypes = dfSurreyTypes.loc[(dfSurreyTypes["contains_pals"] == 0) & ( dfSurreyTypes["nolocal_pals"] == 0) ]
dfSurreyTypes = dfSurreyTypes.drop(["x", "contains_pals", "nolocal_pals"], 1)

dfSurreyPeople = pd.read_csv(inputfileSC, sep=',')
dfSurreyPeople = dfSurreyPeople.drop(["Unnamed: 0"], 1)
dfSurreyPeople = dfSurreyPeople.rename(index=str, columns={"Regiment": "regiment"})

dfMerged = pd.merge(dfSurreyPeople, dfSurreyTypes, how= "inner" , on= "regiment")

dfMerged.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	
