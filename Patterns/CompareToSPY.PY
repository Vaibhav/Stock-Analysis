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
startDate = ""
givenStock = {}

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
		newDate = datetime.strptime(date, "%Y-%m-%d")
		tmp.append(open)
		tmp.append(high)
		tmp.append(low)
		tmp.append(close)
		tmp.append(volume)
		tmp.append(adjclose)
		givenStock[newDate] = tmp
		
		
		
		
def AskUser():
	global ticker, startDate
	if version < 3:
		ticker = raw_input("Please enter a ticker...\n")
		print("Do you want to specify a date? (Y/N) ")
		needDate = raw_input()
		if needDate.startswith("y") or needDate.startswith("Y"):
			start = raw_input("When do you want to start comparison? (YYYY-MM-DD)  \n")
			# startDate = datetime.strptime(start, "%Y-%m-%d")
			startDate = start
		else:
			# startDate = datetime.strptime("2009-01-02", "%Y-%m-%d")
			startDate = "2009-01-02"
		return ticker 
	else:
		ticker = input("Please enter a ticker...\n")
		print("Do you want to specify a date? (Y/N) \n")
		needDate = input()
		if needDate.startswith("y") or needDate.startswith("Y"):
			start = input("When do you want to start comparison? (YYYY-MM-DD) \n")
			startDate = datetime.strptime(start, "%Y-%m-%d")
		else:
			startDate = datetime.strptime("2009-01-02", "%Y-%m-%d")
		return ticker 
			
			
			
			
		
if __name__ == '__main__':
	theTicker = AskUser()
	getStockData(theTicker)
