#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Merging Links
# 2017 06 07


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
inputfile = ["SCServiceLinks/SCLinkServiceRec" + L + str(k) + ".csv"  for L in ["A","B","C","D","E","F","G","H"] for k in range(0,30) ]

# what is our output?
outputfile = "SCServiceMerged.csv"

# Read in the data
df = pd.read_csv(inputfile[0], sep =',')

for i in range(1,len(inputfile) + 1):
	try:
		dfa = pd.read_csv(inputfile[i], sep =',') 
		df = df.append(dfa)
	except:
		continue


print len(df)

df.drop(df.columns[0], axis=1, inplace=True)
df.reset_index(inplace = True,drop= True)


def cleaner(x):
	out = x.replace('"', '')
	out = out.replace("[", "['")
	out = out.replace("]", "']")
	out = out.replace(", ", "', '")
	out = out.replace("['']", '')
	return out
df["Links"] = df["Links"].apply(cleaner)





df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	

print "Done :) "
