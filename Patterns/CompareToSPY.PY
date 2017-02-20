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

try:
    input = raw_input
except NameError:
    pass

now = datetime.now()
DateNow = str(now.year) + "-" + str(now.month) + "-" + str(now.day);

SPY = {}
ticker = ""
startDate = ""
counter1 = 1
counter2 = 0
SPYdata = []
givenStock = []

# a = index of list in list of lists 
# b = index of element in the list 
# [a, b]
def findItem(theList, item):
   return [(ind, theList[ind].index(item)) for ind in xrange(len(theList)) if item in theList[ind]]


def getSP500():
	global SPY, SPYdata
	with open('s-and-p-500-2009.csv', 'r') as source:
		rdr = csv.reader(source)
		next(rdr, None)
		for r in rdr:
			tmp = []
			date = r[0] # datetime.strptime(r[0], "%Y-%m-%d")
			open = float(r[1])
			high = float(r[2])
			low = float(r[3])
			close = float(r[4])
			volume = int(r[5])
			adjclose =  float(r[6])
			tmp.append(date)
			tmp.append(open)
			tmp.append(high)
			tmp.append(low)
			tmp.append(close)
			tmp.append(adjclose)
			tmp.append(volume)
			SPYdata.append(tmp)
			# SPY[date] = tmp
	return SPYdata




def  getStockData(theTicker):
	global startDate, givenStock
	stock = Share(theTicker)
	print("Getting Data for ... " + theTicker)
	print(startDate)
	data = stock.get_historical(startDate, DateNow)
	for d in data:
		tmp = []
		volume = int(d['Volume'])
		adjclose = float(d['Adj_Close'])
		high = float(d['High'])
		low = float(d['Low'])
		close = float(d['Close'])
		date = d['Date']
		open = float(d['Open'])
		# newDate = datetime.strptime(date, "%Y-%m-%d")
		tmp.append(date)
		tmp.append(open)
		tmp.append(high)
		tmp.append(low)
		tmp.append(close)
		tmp.append(adjclose)
		tmp.append(volume)
		givenStock.append(tmp)
	return givenStock

	
# takes in datetime 
def openUpDown(theDate, data):
	today = theDate.strftime("%Y-%m-%d")
	tmp = theDate - timedelta(days=1);
	yesterday = tmp.strftime("%Y-%m-%d")
	ind = findItem(data, today)
	ind2 = findItem(data, yesterday)
	point1 = data[ind[0]]
	point2 = data[ind2[0]]
	

	

def AskUser():
	global ticker, startDate
	ticker = input("Please enter a ticker...\n")
	print("Do you want to specify a date? (Y/N) \n")
	needDate = input()
	if needDate.startswith("y") or needDate.startswith("Y"):
		start = input("When do you want to start comparison? (YYYY-MM-DD) \n")
		# startDate = datetime.strptime(start, "%Y-%m-%d")
		startDate = start
	else:
		# startDate = datetime.strptime("2009-01-02", "%Y-%m-%d")
		startDate = "2009-01-02"
	return ticker 
	
	
	
if __name__ == '__main__':
	theTicker = AskUser()
	getStockData(theTicker)
