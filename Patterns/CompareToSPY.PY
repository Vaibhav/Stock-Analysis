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
	range = xrange
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
   return [(ind, theList[ind].index(item)) for ind in range(len(theList)) if item in theList[ind]]


def getSP500():
	with open('s-and-p-500-2009.csv', 'r') as source:
		rdr = csv.reader(source)
		next(rdr, None)
		for r in rdr:
			tmp = []
			date = r[0] # datetime.strptime(r[0], "%Y-%m-%d")
			day_open = float(r[1])
			high = float(r[2])
			low = float(r[3])
			close = float(r[4])
			volume = int(r[5])
			adjclose =  float(r[6])
			tmp.append(date)
			tmp.append(day_open)
			tmp.append(high)
			tmp.append(low)
			tmp.append(close)
			tmp.append(adjclose)
			tmp.append(volume)
			SPYdata.append(tmp)
			# SPY[date] = tmp
	return SPYdata




def getStockData(theTicker):
	global startDate
	print("Getting Data for ... " + theTicker)
	stock = Share(theTicker)
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
def dayUpDown(theDate, data):
	today = theDate.strftime("%Y-%m-%d")
	ind = findItem(data, today)
	if len(ind) < 1:
		return 0
	indx = ind[0][0]
	point = data[indx]
	open = point[1]
	close = point[5]
	
	if close <	open:
		return 1
	elif close == open:
		return 0
	else:
		return -1

	
# takes in datetime 
def closeUpDown(theDate, data):
	today = theDate.strftime("%Y-%m-%d")
	tmp = theDate - timedelta(days=1);
	yesterday = tmp.strftime("%Y-%m-%d")
	ind = findItem(data, today)
	ind2 = findItem(data, yesterday)
	if len(ind) < 1 or len(ind2) < 1:
		return 0
	indx = ind[0][0]
	indx2 = ind2[0][0]
	point1 = data[indx]
	point2 = data[indx2]
	close1 = point1[5]
	close2 = point2[5]
	if close1 <	close2:
		return 1
	elif close2 == close1:
		return 0
	else:
		return -1

	
# takes in datetime 
def openUpDown(theDate, data):
	today = theDate.strftime("%Y-%m-%d")
	tmp = theDate - timedelta(days=1);
	yesterday = tmp.strftime("%Y-%m-%d")
	ind = findItem(data, today)
	ind2 = findItem(data, yesterday)
	if len(ind) < 1 or len(ind2) < 1:
		return 0
	indx = ind[0][0]
	indx2 = ind2[0][0]
	point1 = data[indx]
	point2 = data[indx2]
	open1 = point1[1]
	close2 = point2[5]
	if close2 <	open1:
		return 1
	elif close2 == open1:
		return 0
	else:
		return -1
	

	

def AskUser():
	global ticker, startDate
	ticker = input("Please enter a ticker...\n")
	ticker = ticker.upper()
	print("Do you want to specify a date? (Y/N) ")
	needDate = input()
	if needDate.startswith("y") or needDate.startswith("Y"):
		start = input("When do you want to start comparison? (YYYY-MM-DD) ")
		# startDate = datetime.strptime(start, "%Y-%m-%d")
		startDate = start
	else:
		# startDate = datetime.strptime("2009-01-02", "%Y-%m-%d")
		startDate = start = "2009-01-02"
	return ticker, start
	
	
	
if __name__ == '__main__':
	SPYdata = getSP500()
	theTicker, start = AskUser()
	givenStock = getStockData(theTicker)
	givenStock.reverse()
	
length = len(SPYdata)
print(length)
length = len(givenStock)
print(length)

dayUp = 0
dayDown = 0
dayNeutral = 0

openUp = 0
openDown = 0
openNeutral = 0

closeUp = 0
closeDown = 0
closeNeutral = 0



for i in SPYdata:
	curDate = i[0]
	newDate = datetime.strptime(curDate, "%Y-%m-%d")
	j = dayUpDown(newDate, SPYdata)
	k = closeUpDown(newDate, SPYdata)
	l = openUpDown(newDate, SPYdata)
	if j == 1:
		dayUp += 1
	elif j == -1:
		dayDown += 1
	else:
		dayNeutral += 1
	
	if k == 1:
		closeUp += 1
	elif k == -1:
		closeDown += 1
	else:
		closeNeutral += 1
		
	if l == 1:
		openUp += 1
	elif l == -1:
		openDown += 1
	else:
		openNeutral += 1

"{0:.2f}".format(13.949999999999999)

print("=====================================================================")
print("==========================" + " S&P 500 " + "======================================")
print("=====================================================================") 
print("Up Days: " + str(dayUp) + "   " + "{0:.2f}".format(100 * float(dayUp)/float(length)) + "%")
print("Down Days: " + str(dayDown) + "   " + "{0:.2f}".format(100 * float(dayDown)/float(length)) + "%")
print("Neutral Days: " + str(dayNeutral) + "   " + "{0:.2f}".format(100 * float(dayNeutral)/float(length)) + "%")


print("Up Open Days: " + str(openUp) + "   " + "{0:.2f}".format(100 * float(openUp)/float(length)) + "%")
print("Down Open Days: " + str(openDown) + "   " + "{0:.2f}".format(100 * float(openDown)/float(length)) + "%")
print("Neutral Open Days: " + str(openNeutral) + "    " + "{0:.2f}".format(100 * float(openNeutral-1)/float(length)) + "%")


print("Up Close Days: " + str(closeUp) + "    " + "{0:.2f}".format(100 * float(closeUp)/float(length)) + "%")
print("Down Close Days: " + str(closeDown) + "    " + "{0:.2f}".format(100 * float(closeDown)/float(length)) + "%")
print("Neutral Close Days: " + str(closeNeutral) + "   " + "{0:.2f}".format(100 * float(closeNeutral-1)/float(length)) + "%")
print("=====================================================================")

dayUp = 0
dayDown = 0
dayNeutral = 0

openUp = 0
openDown = 0
openNeutral = 0

closeUp = 0
closeDown = 0
closeNeutral = 0
j  = k = l = 0
test = 0
		
for n in givenStock:
	if test == 0:
		test += 1
		continue
	curDate = n[0]
	newDate = datetime.strptime(curDate, "%Y-%m-%d")
	j = dayUpDown(newDate, givenStock)
	k = closeUpDown(newDate, givenStock)
	l = openUpDown(newDate, givenStock)
	if j == 1:
		dayUp += 1
	elif j == -1:
		dayDown += 1
	else:
		dayNeutral += 1
	
	if k == 1:
		closeUp += 1
	elif k == -1:
		closeDown += 1
	else:
		closeNeutral += 1
		
	if l == 1:
		openUp += 1
	elif l == -1:
		openDown += 1
	else:
		openNeutral += 1

		
print("=====================================================================")		
print("==========================" + theTicker + "======================================")
print("=====================================================================") 
print("Up Days: " + str(dayUp) + "    " + "{0:.2f}".format(100 * float(dayUp)/float(length)) + "%")
print("Down Days: " + str(dayDown) + "    " + "{0:.2f}".format(100 * float(dayDown)/float(length)) + "%")
print("Neutral Days: " + str(dayNeutral) + "    " + "{0:.2f}".format(100 * float(dayNeutral)/float(length)) + "%")


print("Up Open Days: " + str(openUp) + "    " + "{0:.2f}".format(100 * float(openUp)/float(length)) + "%")
print("Down Open Days: " + str(openDown) + "    " + "{0:.2f}".format(100 * float(openDown)/float(length)) + "%")
print("Neutral Open Days: " + str(openNeutral) + "    " + "{0:.2f}".format(100 * float(openNeutral-1)/float(length)) + "%")


print("Up Close Days: " + str(closeUp) + "    " + "{0:.2f}".format(100 * float(closeUp)/float(length)) + "%")
print("Down Close Days: " + str(closeDown) + "    " + "{0:.2f}".format(100 * float(closeDown)/float(length)) + "%")
print("Neutral Close Days: " + str(closeNeutral) + "    " + "{0:.2f}".format(100 * float(closeNeutral-1)/float(length)) + "%")
print("=====================================================================")