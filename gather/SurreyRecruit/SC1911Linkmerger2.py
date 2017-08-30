# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:24:08 2017

@author: jonasmg
"""

#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Merging Links
# 2017 06 25


#########################
# "administrative stuff"

from __future__ import division

import pandas as pd

from os import chdir


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/input/'
chdir(directory)

# what is our input?
inputfile = ["SCLinks/SC1911NewRec" + L + ".csv"  for L in ["A","B","C","D","E","F","G","H", "I", "J","K"]]

# what is our output?
outputfile = "SC1911Merged2.csv"

# Read in the data
df = pd.read_csv(inputfile[0], sep =',')

for i in range(1,len(inputfile) + 1):
	try:
		dfa = pd.read_csv(inputfile[i], sep =',') 
		df = df.append(dfa)
	except:
		continue



df.drop(df.columns[0], axis=1, inplace=True)
df.reset_index(inplace = True,drop= True)

df = df[df["Links"].notnull()]


df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	
