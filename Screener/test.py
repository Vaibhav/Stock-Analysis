from datetime import datetime, timedelta
import sys
import time

from yahoo_finance import Share

masterlist = [] 
now = datetime.now()
theDate = str(now.year) + "-" + str(now.month) + "-" + str(now.day);

def analyze(dma10, dma20, ticker):
	tenDayAvg = sum(dma10) / float(len(dma10))
	twentyDayAvg = sum(dma20) / float(len(dma20))
	print tenDayAvg
	print twentyDayAvg
	theRange = 0.005 * tenDayAvg
	if tenDayAvg - theRange < twentyDayAvg or twentyDayAvg < tenDayAvg + theRange:
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
	except:
		return 0,0
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
	dma10, dma20 = get_ma(s)
	if dma10 == 0 or dma20 == 0:
		continue
	else:
		print s
		analyze(dma10, dma20, s)

print masterlist