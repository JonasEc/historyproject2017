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
import re
import datetime


########################
# Exec Decisions

# Infantry: 0
# Cavalry: 1
# Artillery: 2
# Labour: 3 
# Engineer: 4
# Training/Reserve: 5
# Other: 6


#####################
# Aide Memoires:




#####++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++################


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# what is our input?
inputfile = "output/listofregiments.csv"

# what is our output?
outputfile = "output/listofregimentsTyped.csv"

# Read in the data
df = pd.read_csv(inputfile, sep =',')



#########################
# The Regex hunt

def Searcher(x):
	Inf1 = re.search("Fusilier",x)
	Inf2 = re.search("Rifles",x)
	Inf3 = re.search("Infantry",x)

	Cav1 = re.search("Dragoon",x)
	Cav2 = re.search("Hussar", x)
	Cav3 = re.search("Lancer",x)
	Cav4 = re.search("Caval",x)
	Cav5 = re.search("Horse",x)
	Cav6 = re.search("Life",x)


	Art1 = re.search("Artillery",x)

	Lab1 = re.search("Labour",x)
	Lab2 = re.search("Service",x)
	Lab3 = re.search("Supply",x)
	Lab4 = re.search("Ordinance",x)
	Lab5 = re.search("Ordanance",x)
	Lab6 = re.search("Ordinance",x)
	Lab7 = re.search("Work",x)
	Lab8 = re.search("Transport",x)

	Eng1 = re.search("Engineer",x)

	Res1 = re.search("Training",x)
	Res2 = re.search("Special",x)
	Res3 = re.search("Reserve",x)

	Other2 = re.search("Cycl",x)
	Other3 = re.search("Veti",x)
	Other4 = re.search("Medic",x)
	Other5 = re.search("Police",x)
	Other6 = re.search("Officer",x)
	Other7 = re.search("Cadet",x)
	Other8 = re.search("School",x)
	Other9 = re.search("Boy",x)
	Other10 = re.search("Pay",x)
	Other11 = re.search("Depot",x)
	Other12 = re.search("Pay",x)
	Other13 = re.search("Provi",x)
	Other14 = re.search("Staff",x)
	Other15 = re.search("Fly",x)
	Other16 = re.search("Nav",x)
	Other17 = re.search("Ambul",x)
	Other18 = re.search("Trade",x)
	Other19 = re.search("Poly",x)
	Other20 = re.search("Test",x)






	if Inf1 or Inf2 or Inf3:
		return 0
	elif Cav1 or Cav2 or Cav3 or Cav4 or Cav5 or Cav6:
		return 1
	elif Art1:
		return 2
	elif Lab1 or Lab2 or Lab3 or Lab4 or Lab5 or Lab6  or Lab7 or Lab8:
		return 3
	elif Eng1:
		return 4
	elif Res1 or Res2 or Res3:
		return 5
	elif (Other2 or Other3 or Other4 or Other5 or Other6 or Other7 or Other8 or Other9 or Other19 or Other20
	or Other10 or Other11 or Other12 or Other13 or Other14 or Other15 or Other16 or Other17 or Other18):
		return 6
	else:
		return 0

df["Type"] = df["Regiment"].apply(Searcher)

df["Type"]=df["Type"].astype('int')

df.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')	




## let me know when all is done
print 'done! :)' 
