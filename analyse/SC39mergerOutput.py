#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project



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
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our input?

inputfile = ["output/SC1939data/SC1939dataExtra"  + k +".csv" for k in ["A","B","C","D","E","F"]]
#inputfile = ["output/SCpeople/SCdataFinal1.csv"]
maxInput = len(inputfile)

# what is our output?
outputfile = "output/SC1939dataFullExtra.csv"

# Read in the data
dfExtra = pd.read_csv(inputfile[0], sep =',')

for i in range(1,len(inputfile)+1):
	try:
		dfa = pd.read_csv(inputfile[i], sep =',') 
		dfExtra = dfExtra.append(dfa)
	except:
		continue



dfExtra = dfExtra.drop("Unnamed: 0")

########################
# print some sumamry stats


print len(dfExtra)
dfExtra.drop_duplicates(keep="first", inplace=True)
print len(dfExtra)

important = ["ID","TargetTNA", "TNA", "Members", "FirstName","LastName","Sex","Occupation","DOB","Address1", "Address2"]
otherVarsPre = [("TNA" + str(k), "FirstName" + str(k),"LastName"+ str(k),"Sex"+ str(k),"Occupation"+ str(k),"DOB"+ str(k)) for k in range(1,14)]
otherVars =  [otherVarsPre[i][j] for i in range(len(otherVarsPre)) for j in range(6)]
reordering = important + otherVars

dfExtra = dfExtra[reordering]

### save to csv
dfExtra.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	



## let me know when all is done
print 'done! :)' 