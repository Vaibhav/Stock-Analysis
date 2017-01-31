from datetime import datetime, timedelta
import sys

from yahoo_finance import Share

masterlist = [] 
now = datetime.now()
theDate = str(now.year) + "-" + str(now.month) + "-" + str(now.day);

def analyze(dma10, dma20, ticker):
	tenDayAvg = sum(dma10) / float(len(dma10))
	twentyDayAvg = sum(dma20) / float(len(dma20))
	print tenDayAvg
	print twentyDayAvg
	theRange = 0.02 * tenDayAvg
	if tenDayAvg - theRange < twentyDayAvg or twentyDayAvg < tenDayAvg + theRange:
		masterlist.append(ticker)


def get_ma(stock):
	prices_10 = []
	prices_20 = []
	stock = Share(stock)
	dma_10 = now - timedelta(days=30)
	date10 = str(dma_10.year) + "-" + str(dma_10.month) + "-" + str(dma_10.day);
	data = stock.get_historical(date10, theDate)
	count = 0
	for theData in data:
		if count < 10:
			count = count + 1
			prices_10.append(float(theData['Adj_Close']))
		else:
			continue
	print prices_10
	count = 0
	for theData in data:
		if count < 20:
			count = count + 1
			prices_20.append(float(theData['Adj_Close']))
		else:
			continue
	print prices_20
	return prices_10, prices_20
	

stocks = ['AMD']
for s in stocks:
	dma10, dma20 = get_ma(s)
	analyze(dma10, dma20, s)

print masterlist