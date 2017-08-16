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


## EXEC:
# ID = MC+ numbers

##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfile = ["output/MCPdata/MCPdata" + str(k) +".csv" for k in range(1,14)]
#inputfile = ["output/SCpeople/SCdataFinal1.csv"]
maxInput = len(inputfile)

# what is our output?
outputfile = "data/MCPComplete.csv"

# Read in the data
df = pd.read_csv(inputfile[0], sep =',')

for i in range(1,len(inputfile)+1):
	try:
		dfa = pd.read_csv(inputfile[i], sep =',') 
		df = df.append(dfa)
	except:
		continue

## make ID:
length = len(df)
IDlist = ["MC" + str(i) for i in range(length)]
IDcol = pd.Series(IDlist,index=df.index)

df["ID"] = IDcol


########################
# print some sumamry stats

print len(df)


### save to csv
df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print 'done! :)' 