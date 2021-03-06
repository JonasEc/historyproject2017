#############################################
# Jonas Mueller Gastell & Melanie Wallskog
# History Project

#############################################
# Log Into Website and Save the Cookies: LivesOfTheFirstWorldWar
# 2017 05 19


#########################
# "administrative stuff"

from __future__ import division

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import mechanize
import cookielib 
import urllib2
import pickle


import pandas as pd
from bs4 import BeautifulSoup
from os import chdir
import re
from unidecode import unidecode
import time



#################### 
# Data Storage, Output and Input

# select correct directory
directory = '/home/jonasmg/Prog/scrapinghistory/'
chdir(directory)



######################
# Selenium Set up

## log into findmypast.com
driver = webdriver.Firefox()
driver.get('https://livesofthefirstworldwar.org/login')

time.sleep(5)

#driver.find_element_by_xpath('//*[@id="join-nav-link"]').click

time.sleep(5)

username = driver.find_element_by_id("EmailAddress")
password = driver.find_element_by_id("Password")

username.send_keys("jonas.muellergastell@gmail.com")
password.send_keys("History2017!")

driver.find_element_by_id("login-submit").click()

# allow it to actually load...
time.sleep(15)

## get the cookies
cookies = driver.get_cookies()

### dump them to pickles
pickle.dump( cookies , open("cookies/cookiesLFWW.pkl","wb"))


## close the browser when all is done
driver.quit()
print 'done! :)' # to let me know its done 




