from __future__ import division

import mechanize
import cookielib 
import urllib2
import pickle

import pandas as pd
from bs4 import BeautifulSoup
from os import chdir
import re
from unidecode import unidecode
from math import ceil


# # authenticate 
# driver.open('https://www.findmypast.com/sign-in') 
# # these two come from the code you posted
# # where you would normally put in your username and password
# driver.select_form(nr=0)
# driver[ "emailAddress" ] = "jonas.muellergastell@gmail.com"
# driver[ "password" ] = "History2017!"
# req = driver.submit() 



for s_cookie in cookie:
	try:
		cj.set_cookie(cookielib.Cookie(version = 0, name = s_cookie['name'], value = s_cookie['value'], port = '80', port_specified = False, domain = s_cookie['domain'], domain_specified = True, domain_initial_dot = False, path = s_cookie['path'], path_specified = True, secure = s_cookie['secure'], expires = s_cookie['expiry'], discard = False, comment = None, comment_url = None, rest = None, rfc2109 = False))
	except KeyError:
		cj.set_cookie(cookielib.Cookie(version = 0, name = s_cookie['name'], value = s_cookie['value'], port = '80', port_specified = False, domain = s_cookie['domain'], domain_specified = True, domain_initial_dot = False, path = s_cookie['path'], path_specified = True, secure = s_cookie['secure'], expires = None, discard = False, comment = None, comment_url = None, rest = None, rfc2109 = False))
