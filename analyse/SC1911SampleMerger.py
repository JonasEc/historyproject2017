# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 18:25:08 2017

@author: jonasmg
"""

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




##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory'
chdir(directory)

inputfile1 = "data/SC1911New.csv"
inputfile2 = "data/SCBaseSampleMerged2.csv"

outputfileF = "data/SCBaseSampleWith1911.csv"
outputfileS = "data/SCBaseSampleWith1911Select.csv"


df1 = pd.read_csv(inputfile1, sep =',')
df2 = pd.read_csv(inputfile2, sep =',')

df1 = df1.drop("Unnamed: 0", axis=1)
df2 = df2.drop("Unnamed: 0", axis=1)

dfMerged = pd.merge(df1, df2, how= "right" , on= "ID")
dfMerged1911 = dfMerged[dfMerged["FirstName_x"].notnull()]

dfMerged.to_csv(outputfileF,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	
dfMerged1911.to_csv(outputfileS,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	
