#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Merging Links
# 2017 07 17


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
inputfile = ["MCLinks/MCNonPals/MCNonPalsLinks" + str(k) + ".csv"   for k in range(0,17) ]

# what is our output?
outputfile = "MCLinks/MCNonPalsMerged.csv"

# Read in the data
df = pd.read_csv(inputfile[0], sep =',')

for i in range(1,len(inputfile) + 1):
	try:
		dfa = pd.read_csv(inputfile[i], sep =',') 
		df = df.append(dfa)
	except:
		continue


li = df["Links"].tolist()

se = set(li)

li = list(se)

df2 = pd.DataFrame(li, columns = ["Links"])




df2.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	

print "Done :) "
