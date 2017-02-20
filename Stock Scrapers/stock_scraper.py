##############
'''
   Version 2.0
   Author: Vaibhav Khaitan
   Date: Feb 2017
   Scrape Stock data using Yahoo Finance API
   Script asks user for Stock symbol and starting year
   Script outputs a CSV file with open/high/low/close/volume for given stock
'''
##############
import timeit
import datetime
import pandas as pd
import shutil
import csv
import os
from yahoo_finance import Share
from datetime import datetime



def getStockData(theTicker, startDate):
	stock = Share(theTicker)
	print("Getting Data for ... " + theTicker)
	now = datetime.now()
	DateNow = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
	data = stock.get_historical(startDate, DateNow)
	stockData = [['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
	for d in data:
		tmp = []
		volume = int(d['Volume'])
		adjclose = float(d['Adj_Close'])
		high = float(d['High'])
		low = float(d['Low'])
		close = float(d['Close'])
		date = d['Date']
		open = float(d['Open'])
		tmp.append(date)
		tmp.append(open)
		tmp.append(high)
		tmp.append(low)
		tmp.append(close)
		tmp.append(adjclose)
		tmp.append(volume)
		stockData.append(tmp)
	return stockData


def writeToFile(data, f):
	tmp_df = pd.DataFrame(data)
	tmp_df.to_csv(f, index=False, header=False)
	'''
	with open(f, 'w'):
		writer = csv.writer(f)
		writer.writerows(data, delimiter=',')
	'''


	
def getInput():
	#Ask user to input ticker
	the_stock = raw_input('Enter Stock Ticker Code: \n')
	the_stock = the_stock.upper().strip()

	#Asks user to input starting year 
	year = raw_input('Enter starting year: \n')
	the_year = year.strip()
	year = year.strip()

	f = the_stock + '_' + year + '-2017.csv';
	return the_stock, year, f
	


stock, year, f = getInput()
year = year + "-01-01"
stockData = getStockData(stock, year)
print stockData	
writeToFile(stockData, f)

#Saves file in Datasets folder
shutil.move(f, "Datasets/")
print "Finished writing - Check Datasets Folder"
	
######################################################
