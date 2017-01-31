'''
Author: Vaibhav Khaitan
Date: 1/30/2017
Description: Script attempts to filter out stocks which can be used for quantified moving average strategy. 
'''
from datetime import datetime, timedelta
import sys
import time

from yahoo_finance import Share

masterlist = []
minorlist = [] 
now = datetime.now()
theDate = str(now.year) + "-" + str(now.month) + "-" + str(now.day);

def analyze(dma10, dma20, dma50, ticker):
	tenDayAvg = sum(dma10) / float(len(dma10))
	twentyDayAvg = sum(dma20) / float(len(dma20))
	print tenDayAvg
	print twentyDayAvg
	theRange = 0.02 * tenDayAvg
	if tenDayAvg - theRange < twentyDayAvg and twentyDayAvg < tenDayAvg + theRange:
		minorlist.append(ticker)
		if tenDayAvg - theRange < dma50 and dma50 < tenDayAvg + theRange:
			masterlist.append(ticker)


def get_ma(stock):
	prices_10 = []
	prices_20 = []
	stock = Share(stock)
	dma_10 = now - timedelta(days=30)
	date10 = str(dma_10.year) + "-" + str(dma_10.month) + "-" + str(dma_10.day);
	time.sleep(0.5)
	try:
		data = stock.get_historical(date10, theDate)
		prices_50 = stock.get_50day_moving_avg()
	except:
		return 0,0,0
	count = 0
	for theData in data:
		if count < 10:
			count = count + 1
			prices_10.append(float(theData['Adj_Close']))
		else:
			continue
	count = 0
	for theData in data:
		if count < 20:
			count = count + 1
			prices_20.append(float(theData['Adj_Close']))
		else:
			continue
	print prices_50
	return prices_10, prices_20, prices_50
	

	
def read_tickers():
    print("Reading tickers from \"tickers.txt\":")
    f = open("tickers2.txt", 'r')
    names = []
    # read tickers from tickers.txt
    for line in f:
    	line = line.strip('\n')
    	line = line.upper()
    	line = line.strip('\t')
    	names.append(line)
    print(names)
    return names


stocks = read_tickers()
for s in stocks:
	dma10, dma20, dma50 = get_ma(s)
	if dma10 == 0 or dma20 == 0 or dma50 == 0:
		continue
	else:
		print s
		analyze(dma10, dma20, dma50, s)


print "Major List:"
print masterlist
print "Minor List"
print minorlist
