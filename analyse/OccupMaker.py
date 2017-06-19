#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# First stab at creating a useful subsample: the unit type regex
# 2017 05 24


#########################
# "administrative stuff"

from __future__ import division

import pandas as pd
from bs4 import BeautifulSoup

from os import chdir

from collections import Counter





#####++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++################


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfile = "data/SCSample2.csv"

# what is our output?
outputfile = "output/listofoccupations.csv"

# Read in the data
df = pd.read_csv(inputfile, sep =',')



#########################

occupationlist = df["Occupation"].tolist()

output = Counter(occupationlist).most_common()

output = pd.DataFrame.from_dict(output)

output.columns = ['OccupationName','NumberOfOccurences']

output.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	




## let me know when all is done
print 'done! :)' 
