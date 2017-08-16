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
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfile = 'input/SC1939Merged.csv'
outputfile = 'input/SC1939LinkSample.csv'
outputfile2 = 'input/SC1939LinkSampleExtraNonPals.csv'

# Read in the data
df = pd.read_csv(inputfile, sep =',')


df.drop(df.columns[0], axis=1, inplace=True)


df.sort_values(["Pal","Numbers","Links"], axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last')

df = df[df["Links"].notnull()]
df = df[df["Numbers"] > 5]


print(df['Pal'].value_counts())

df.reset_index(inplace = True,drop= True)

dfPals = df[:581]
dfNonPals = df[581:1081]

dfOut = dfPals.append(dfNonPals)

dfOut2 = df[1081:]
#
#
#
#
#
dfOut.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	

dfOut2.to_csv(outputfile2,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	
#
#print("Done :) ")
