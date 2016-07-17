##############
'''
   Author: Vaibhav Khaitan
   Date: July 2016
   Scrape Stock data using Yahoo Finance API
   Script asks user for Stock symbol and starting year
   Script outputs a CSV file with open/high/low/close/volume for given stock
'''
##############

import datetime
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import DataFrame
from pandas_datareader import data as dr
from pyalgotrade.barfeed import yahoofeed

#NYSE TOP 40 Stocks
#Read 2 stocks

f = open('stock.txt', 'r')
symbols_list = [f.readline()[:-1],f.readline()]

print symbols_list

if os.path.isfile(symbols_list[0]+'-'+symbols_list[1]+'.csv')==False: 
    symbols=[]
    now = datetime.datetime.now()
    is_today = 0;
    for ticker in symbols_list:
        print ticker
        i,j = 1,1
        for i in range (1,13):
            print i
            if (is_today == 1):
                break;
            
            for j in range(1,21):

                if(now.month == i+1 && now.day == j+1):
                    is_today = 1;
                    break;
                
                print j
                r = DataReader(ticker, "yahoo", start=datetime.datetime(2016, i, j))
                # add a symbol column
                r['Symbol'] = ticker 
                symbols.append(r)
                j += 1
    
            i += 1
			
    # concatenate all the dataframes
    df = pd.concat(symbols)
    # create an organized cell from the new dataframe
	
    cell= df[['Symbol','Open','High','Low','Adj Close','Volume']]
    cell.reset_index().sort(['Symbol', 'Date'], ascending=[1,1]).set_index('Symbol').to_csv(symbols_list[0]+'-'+symbols_list[1]+'.csv', date_format='%d/%m/%Y')

    inFile = open(symbols_list[0]+'-'+symbols_list[1]+'.csv', 'r')
    outFile =  open(symbols_list[0]+' to '+symbols_list[1]+'.csv', 'w')
    
    listLine = []
	
    for line in inFile:

        if line in listLine:
            continue
        else:
            outFile.write(line)
            listLine.append(line)
		
    outFile.close()
    inFile.close()
    os.remove(symbols_list[0]+'-'+symbols_list[1]+'.csv')
	
    print "Finished writing"
	
	

	
	
