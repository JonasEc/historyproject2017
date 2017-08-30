#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 16:14:10 2017

@author: jonasmg
"""

#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project


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

inputfile = "data/SC1939FirstSample.csv"



# what is our output?
outputfile = "data/SC1939FirstSampleFixed.csv"
outputfile2 = "data/SC1939FirstSampleJustOccup.csv"


# Read in the data
df = pd.read_csv(inputfile, sep =',')

df = df.drop("Unnamed: 0", 1)
df = df.drop("Unnamed: 0.1", 1)

df["RoleIfNotHouseHold"] = "0"


def tidyRole(row):
    role = row["DOB"]
    listRoles = ["Inmate","Patient","P","patient","Visitor","I","V","inmate","visitor","S","Servant","servant"]
    if  role in listRoles:
        row["RoleIfNotHouseHold"] = role
        row["DOB"] = row["Sex"]
        row["Sex"] = row["Occupation_x"]
        row["Occupation_x"] = row["MaritalStatus"]
        row["MaritalStatus"] = row["Schedule"]
    return row

df = df.apply(tidyRole, axis=1)

#df2 = df.loc[df["TargetTNA"] != df["TNA"]]

df = df.drop(["Schedule","ScheduleSubNumber"], axis = 1)

df.drop_duplicates(keep="first", inplace = True, subset =["TNA", "FirstName_x", "LastName_x","FirstName_y", "LastName_y", "DOB", "BirthDate" ])



def tidyOccup(x):
    if isinstance(x, basestring):
        x =  x.replace("-","") 
        x =  x.replace("?","")
#    x = x.replace("(Heavy Work)", "") 
#    x = x.replace("Heavy Work", "")
#    x = x.replace("Heavy", "")
#    x = x.replace("Heav Wor", "")
#    x= x.replace("H W", "")
#    x= x.replace("(H W)", "")
#    x = x.replace("HW", "")    
#    x = x.replace("(HW)", "")
#    x = x.replace("Hw", "")    
#    x = x.replace("(Hw)", "")
    return x

df["Occupation_x"] = df["Occupation_x"].apply(tidyOccup) 

df = df[df["Occupation_x"] != ""]
df = df[pd.notnull(df["Occupation_x"])]

df3 = df[["ID","Occupation_x","Occupation_y"]]
df.to_csv(outputfile, sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')
df.to_csv(outputfile2, sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')