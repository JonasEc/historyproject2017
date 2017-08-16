#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project


#########################
# "administrative stuff"

from __future__ import division

import pandas as pd
import numpy as np


from os import chdir



##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our input?

inputfile = "output/SC1939dataFull.csv"
inputfile1 = "output/SC1939dataFullExtra.csv"
inputfile2 = "data/SCBaseSampleMerged.csv"



# what is our output?
outputfile = "data/SC1939FirstSample.csv"

# Read in the data
df39 = pd.read_csv(inputfile, sep =',')
df391 = pd.read_csv(inputfile1, sep =',')

#df39 = df39.drop("Unnamed: 0")


df39 = df39.append(df391)

important = ["ID","TargetTNA", "TNA", "Members", "FirstName","LastName","Sex","Occupation","DOB","MaritalStatus","Address1", "Address2", "Schedule", "ScheduleSubNumber"]
otherVarsPre = [("TNA" + str(k), "FirstName" + str(k),"LastName"+ str(k),"Sex"+ str(k),"Occupation"+ str(k),"DOB"+ str(k),"MaritalStatus" + str(k)) for k in range(1,14)]
otherVars =  [otherVarsPre[i][j] for i in range(len(otherVarsPre)) for j in range(7)]
reordering = important + otherVars

df39["MaritalStatus12"] = np.nan
df39["MaritalStatus13"] = np.nan

df39 = df39[reordering]

print len(df39)
df39.drop_duplicates(keep="first", inplace=True)
print len(df39)

dfSurrey = pd.read_csv(inputfile2, sep= ",")

### MERGE
df = pd.merge(df39, dfSurrey, how = 'inner', on = "ID")


### save to csv
df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print 'done! :)' 