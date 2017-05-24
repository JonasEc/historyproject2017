#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# combine female fist name lists
# 2017 05 06


#########################
# "administrative stuff"

from os import chdir
import pandas as pd

directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

malenamesDF1 = pd.read_csv("output/malenames1.csv", sep =',')
malenamesDF2 = pd.read_csv("output/malenames2.csv", sep =',')
malenames1 = malenamesDF1['Firstname'].tolist()
malenames2 = malenamesDF2['Firstname'].tolist()

malenames = malenames1 + list(set(malenames2) - set(malenames1))

outputframe = pd.DataFrame(malenames, columns=["Firstname"])

outputframe.to_csv("input/malefirstnames.csv",sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')
