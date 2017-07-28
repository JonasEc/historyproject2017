#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Creating Sample for Manchester Pals
# 2017 07 24


#########################
# "administrative stuff"
import pandas as pd

from os import chdir


#########################
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)

# filenames
inputfilesMCS = 'data/MCService.csv'
inputfileMCP = 'data/MCPComplete.csv'
inputfileTypes = 'data/ManBattListTyped.csv'

outputfile = 'output/MCServiceForScrape.csv'


########################
# Read in the data

dfService = pd.read_csv(inputfilesMCS, sep =',')
dfPals = pd.read_csv(inputfileMCP, sep=',')
dfBatt = pd.read_csv(inputfileTypes, sep=',')

dfService.drop_duplicates(inplace = True, keep = 'first')

# vars = "FirstName","LastName","ServiceNumber","Age","BirthYear","BirthTown","BirthCounty","ResidenceTown","ResidenceCounty","ResidenceCountry","BirthCountry","Regiment","UnitBattalion","Year"


########################
# clean ServiceRecs

def RegimentDummyMaker(reg):
    regList = reg.split(" ")
    k = 0
    for w in regList:
        if w == "Manchester":
            k = 1
            break
    return k

dfService['Dummy'] = dfService['Regiment'].apply(RegimentDummyMaker)
dfService = dfService[dfService['Dummy'] == 1]
dfService.drop(dfService.columns[16], axis=1, inplace=True)
dfService.drop(dfService.columns[0], axis=1, inplace=True)
dfPals.drop(dfPals.columns[[0,1]], axis=1, inplace=True)
dfPals = dfPals.rename(index=str, columns={"Batallion":"Battalion"})



# drop if not in right battalion type

dfService = pd.merge(dfService, dfBatt, how = 'inner', on = "UnitBattalion")
dfService = dfService[dfService["Type"] == "Pal"]
dfService = dfService.drop('Unnamed: 4', 1)

######################
# merge with Pals data: need to merge many to one
dfMerged = pd.merge(dfService, dfPals, how= "inner" , on= "ID")



## merge identical records by more data

dfMerged.sort_values(["ID", "FirstName_x", "LastName_x", "Year"], ascending=True, inplace = True)

dfMerged["keep"] = 1

#for index in range(len(dfMerged.index)-1):
#    if dfMerged['ID'].iloc[index] == dfMerged['ID'].iloc[index+1] and dfMerged['FirstName_x'].iloc[index] == dfMerged['FirstName_x'].iloc[index+1] and dfMerged['LastName_x'].iloc[index] == dfMerged['LastName_x'].iloc[index+1]:
#        dfMerged["keep"].iloc[index+1] = 0
#        for var in ["Age", "BirthYear","BirthYear", "BirthTown", "BirthCounty", "ResidenceTown", "ResidenceCounty", "ResidenceCountry", "BirthCountry"]:     
#            if dfMerged[var].iloc[index] == "" and dfMerged[var].iloc[index+1] != "":
#                dfMerged[var].iloc[index] = dfMerged[var].iloc[index+1]
#    elif dfMerged["ID"].iloc[index] == dfMerged["ID"].iloc[index+1]:
#        dfMerged["keep"].iloc[index] = 0
#        dfMerged["keep"].iloc[index +1] = 0
#    else:
#        continue
#
#dfMerged = dfMerged[dfMerged["keep"]== 1]       



#    
#dfMerged.drop(["BatNumber","FirstName_y", "LastName_y","ServiceNumber_x","RecordSet","keep","UnitBattalion"], axis=1, inplace=True)
#
#
#dfMerged= dfMerged.rename(index=str, columns={'FirstName_x':"FirstName", 'LastName_x':"LastName", "ServiceNumber_y": "ServiceNumber"})
#
#dfMerged.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')
