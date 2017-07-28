from __future__ import division

import mechanize
import cookielib 

import pandas as pd
from bs4 import BeautifulSoup
from os import chdir
import re
from unidecode import unidecode
from math import ceil
import time
import sys


######################
# Executive Decisions

### how many records max per search type?
maxPage = 76
entries = 20


##################### 
# Data Storage, Output and Input

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)


inputfile = 'input/towns.csv'

df = pd.read_csv(inputfile, sep =',') 

def number(x):
	return int(''.join(element for element in x if element.isdigit()))

def townonly(x):
	return ''.join(element for element in x if element.isalpha())

df["number"] = df["town"].apply(number)
df["town"] = df["town"].apply(townonly)

print df["number"].sum()

df.to_csv("input/townsOnly.csv",sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

