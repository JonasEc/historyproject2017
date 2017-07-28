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


girlnamesDF1 = pd.read_csv("output/girlnames1.csv", sep =',')
girlnamesDF2 = pd.read_csv("output/girlnames2.csv", sep =',')
girlnames1 = girlnamesDF1['Firstname'].tolist()
girlnames2 = girlnamesDF2['Firstname'].tolist()

girlnames = girlnames1 + list(set(girlnames2) - set(girlnames1))

outputframe = pd.DataFrame(girlnames, columns=["Firstname"])

outputframe.to_csv("input/femalefirstnames.csv",sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')
