############################
###
## Vaibhav Khaitan
## February 2017
## Module compares the S&P to the given stock 
## and tries to find any correlation they have.
###
############################

# Starting with 2009 
# Do not want to include the market crash in 2008 since it is outlier data 
# May add a 2008 crash handler in the future

# Date	Open	High	Low	Close	Volume	Adj Close
# 2009-01-02

from datetime import datetime, timedelta
import sys
import time
import csv
from yahoo_finance import Share

version = sys.version_info[0]

now = datetime.now()
DateNow = str(now.year) + "-" + str(now.month) + "-" + str(now.day);

SPY = {}
ticker = ""

def getSP500():
	global SPY
	with open('s-and-p-500-2009.csv', 'r') as source:
		rdr = csv.reader(source)
		next(rdr, None)
		for r in rdr:
			tmp = []
			date = datetime.strptime(r[0], "%Y-%m-%d")
			open = float(r[1])
			high = float(r[2])
			low = float(r[3])
			close = float(r[4])
			volume = int(r[5])
			adjclose =  float(r[6])
			tmp.append(open)
			tmp.append(high)
			tmp.append(low)
			tmp.append(close)
			tmp.append(volume)
			tmp.append(adjclose)
			SPY[date] = tmp
		


	

