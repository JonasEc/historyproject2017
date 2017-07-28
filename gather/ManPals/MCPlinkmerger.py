#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Merging Links
# 2017 07 10


#########################
# "administrative stuff"

from __future__ import division

import pandas as pd

from os import chdir


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/input/'
chdir(directory)

# what is our input?
inputfile = ["MCPLinks" + L + ".csv"  for L in ["A","B","F","L","R","X", "S","Y", "1","2","3", "4"]]

# what is our output?
outputfile = "MCPLinksMerged.csv"

# Read in the data
df = pd.read_csv(inputfile[0], sep =',')

for i in range(1,len(inputfile) + 1):
	try:
		dfa = pd.read_csv(inputfile[i], sep =',') 
		df = df.append(dfa)
	except:
		continue


print len(df)

dfList = df["Links"].tolist()
dfSet = set(dfList)
dfList = list(dfSet)

print len(dfList)

df2 = pd.DataFrame(dfList, columns=["Links"])

df2.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	

print "Done :) "
