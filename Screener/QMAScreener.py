'''
Author: Vaibhav Khaitan
Date: 8/15/2018
Description: Script attempts to filter out stocks which can be used for quantified moving average strategy.
'''
from datetime import datetime, timedelta
import pandas as pd 
from pandas_datareader import data
from iexfinance import Stock, get_historical_data, get_available_symbols

masterlist = []
minorlist = []
now = datetime.now()

rangeResistance = 0.01 # Range resistance level, the range between moving averages
numberOfStocks = 100 # number of stocks to test

def analyze(dma10, dma20, dma50, ticker):
	theRange = 0.01 * dma10
	if dma10 - theRange < dma20 and dma20 < dma10 + theRange:
		minorlist.append(ticker)
		if dma10 - theRange < dma50 and dma50 < dma10 + theRange:
			masterlist.append(ticker)


def get_ma(ticker):
	stock = Stock(ticker)
	start = now - timedelta(days=25)
	try:
		keyStats = stock.get_key_stats()
		if (stock.get_price() < 5):
			return -1,-1,-1
		
		df_hist = get_historical_data(ticker, start=start, end=now, output_format='pandas')
		dma50 = keyStats['day50MovingAvg']
		dma10 = df_hist.tail(10)['close'].mean()
		dma20 = df_hist.tail(20)['close'].mean()
	except:
		return -1,-1,-1
	
	return dma10, dma20, dma50


listOfTickers = get_available_symbols(output_format='pandas')
df = pd.DataFrame(listOfTickers)
df = df.loc[df['type'] == 'cs']
df = df.head(numberOfStocks)

for i,r in df['symbol'].iteritems():
	print("Getting Averages for "+r+"\n")
	dma10, dma20, dma50 = get_ma(r)
	if dma10 == -1 or dma20 == -1 or dma50 == -1:
		continue
	else:
		analyze(dma10, dma20, dma50, r)


print("Major List:")
print(masterlist)
print("Minor List")
print(minorlist)
