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
inputfile = ["SC1911Links/SC1911Rec" + L + str(k) + ".csv"  for L in ["A","B","C","D","E","F","G","H"] for k in range(0,30) ]

# what is our output?
outputfile = "SC1911Merged.csv"

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







df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	

