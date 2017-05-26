import pandas as pd
from os import chdir

# select correct directory
directory = '/Users/jonasmuller-gastell/prog/scrapinghistory/'
chdir(directory)

# our data input file
linkset = ["input/SClinks/merged/SClinksMergedOld.csv"]+ ["input/SClinks/SCpeopleLinksYears" + str(k) + ".csv" for k in range(1,105)] 
 
# what is our output?
output = []
outputfile = "input/SClinks/merged/SClinksMergedFinal.csv"



for link in linkset:
	linksDF = pd.read_csv(link, sep =',')
	linksList = linksDF['Links'].tolist()
	output = output + list(set(linksList) - set(output))

outputframe = pd.DataFrame(output, columns=["Links"])
outputframe.to_csv(outputfile,sep=',', na_rep='', float_format=None, header=True,encoding='utf-8')

print "Done :)"