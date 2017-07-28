#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Merging SC Base Sample with SC Service Records 
# 2017 07 27 


#########################
# "administrative stuff"

from __future__ import division

import pandas as pd

from os import chdir
import re



########################
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfileB = "data/SCBaseSample2.csv"
inputfileS = "data/SCServiceComplete.csv"

# what is our output?
outputfile = "data/SCBaseServiceSample.csv"


########################

dfService = pd.read_csv(inputfileS, sep=",")
dfBase = pd.read_csv(inputfileB, sep=",")

dfBase = dfBase.drop(["Unnamed: 0"], 1)
dfService = dfService.drop(["Unnamed: 0", "Unnamed: 0.1"], 1)

#def ServiceNumCleaner(servicenum):
#    servicenum = "".join([s for s in servicenum if s.isdigit()])
#    return servicenum

#dfService["ServiceNumber"] = dfService["ServiceNumber"].apply(ServiceNumCleaner)

dfMerged = pd.merge(dfService, dfBase, how= "inner" , on= "ID")

dfMerged = dfMerged.loc[(dfMerged["BirthYear_x"] != "-") | (dfMerged["Age_x"].notnull())]

def distanceBirthYear(row):
    if row["BirthYear_x"] != "-":
        imputedBirthYear = int(row["BirthYear_x"])
    else:
	    imputedBirthYear = int(row["Year"]) - int(row["Age_x"])
    row["distanceBirthYear"] = abs(int(row["BirthYear_y"]) - imputedBirthYear)
    return row["distanceBirthYear"]

dfMerged["distanceBirthYear"] = dfMerged.apply(distanceBirthYear, axis = 1)

dfMerged = dfMerged[dfMerged["distanceBirthYear"] <= 2]

dfMerged["keep"] = 1

for index in range(len(dfMerged.index)-1):
    if (dfMerged['ID'].iloc[index] == dfMerged['ID'].iloc[index+1] and dfMerged['FirstName_x'].iloc[index] == dfMerged['FirstName_x'].iloc[index+1] 
    and dfMerged['LastName_x'].iloc[index] == dfMerged['LastName_x'].iloc[index+1] and dfMerged['BirthYear_x'].iloc[index] == dfMerged['BirthYear_x'].iloc[index+1]
    and dfMerged['BirthTown'].iloc[index] == dfMerged['BirthTown'].iloc[index+1]):
        if dfMerged['Year'].iloc[index] >= dfMerged['Year'].iloc[index+1] and dfMerged['Year'].iloc[index+1] < 1914:
            dfMerged["keep"].iloc[index+1] = 0
            for var in ["ResidenceTown", "ResidenceCounty", "ResidenceCountry", "Regiment_x", "UnitBattalion"]:     
                if dfMerged[var].iloc[index] == "" and dfMerged[var].iloc[index+1] != "":
                    dfMerged[var].iloc[index] = dfMerged[var].iloc[index+1]
        elif dfMerged['Year'].iloc[index] < dfMerged['Year'].iloc[index+1] and dfMerged['Year'].iloc[index+1] >= 1914:
            dfMerged["keep"].iloc[index] = 0
            for var in ["ResidenceTown", "ResidenceCounty", "ResidenceCountry", "Regiment_x", "UnitBattalion"]:     
                if dfMerged[var].iloc[index] != "" and dfMerged[var].iloc[index+1] == "":
                    dfMerged[var].iloc[index+1] = dfMerged[var].iloc[index] 
        elif dfMerged['Year'].iloc[index] > dfMerged['Year'].iloc[index+1] and dfMerged['Year'].iloc[index+1] > 1914:
            dfMerged["keep"].iloc[index] = 0
            for var in ["ResidenceTown", "ResidenceCounty", "ResidenceCountry", "Regiment_x", "UnitBattalion"]:     
                if dfMerged[var].iloc[index] != "" and dfMerged[var].iloc[index+1] == "":
                    dfMerged[var].iloc[index+1] = dfMerged[var].iloc[index] 
    elif dfMerged["ID"].iloc[index] == dfMerged["ID"].iloc[index+1]:
        dfMerged["keep"].iloc[index] = 1
        dfMerged["keep"].iloc[index +1] = 1
    else:
        continue


dfMerged = dfMerged[dfMerged["Year"] >= 1914]
dfMerged = dfMerged[dfMerged["keep"] == 1]

dfMerged["keep"] = 0
dfMerged["keepLooser"] = 0
dfMerged["keep3"] = 0 
dfMerged["keep"].loc[(dfMerged["FirstName_x"] == dfMerged["FirstName_y"]) & (dfMerged["BirthCounty_x"] == dfMerged["BirthCounty_y"])] = 1  
dfMerged["keepLooser"].loc[(dfMerged["BirthCounty_x"] == dfMerged["BirthCounty_y"])] = 1  
dfMerged["keep3"].loc[(dfMerged["BirthTown"] == dfMerged["BirthPlace"]) & (dfMerged["BirthCounty_x"] == dfMerged["BirthCounty_y"])] = 1  

dfMerged = dfMerged.loc[(dfMerged["keep"] == 1) | (dfMerged["keepLooser"] == 1) | (dfMerged["keep3"] == 1)]





