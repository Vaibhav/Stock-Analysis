
#Scrapes stock data from Yahoo Finance
import datetime
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import DataFrame
from pandas_datareader import data as dr
from pyalgotrade.barfeed import yahoofeed

month = 12
business_days = 20

months =  ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#Ask user to input ticker
the_stock = raw_input('Enter Stock Ticker Code: \n')
the_stock = the_stock.upper().strip()
symbols_list = [the_stock]
year = raw_input('Enter starting year: \n')
#Ex: 'YHOO','MSFT','ALTR','WDC','KLAC', 'BAC', 'KMI' ,'SUNE', 'HPQ', 'FCX', 'GE', 'PBR', 'BABA', 'ITUB', 'XOM', 'C', 'EMC', 'MPLX', 'CNX' ,'NRG', 'S', 'EPD', 'WMT', 'ORCL'
 
if os.path.isfile(symbols_list[0]+'.csv') == False:
    
    symbols=[]
    now = datetime.datetime.now()
    is_today = 0;
    year = int(year)
    
    for ticker in symbols_list:
        print ticker
        i,j = 0,0

        if(year == now.year and is_today == 1):
                break;
        
        for i in range (0,month):
            print months[i]
                
            if(year == now.year and i+1 == now.month and is_today == 1):
                break;
			
			
            for j in range(0,business_days):

                if(year == now.year and i+1 == now.month and j+1 == now.day):
                    is_today = 1;
                    break;
				
                print j+1
                
                #Use Yahoo Finance API to retrive stock data for given day and month
                temp = dr.DataReader(ticker, "yahoo", start=datetime.datetime(year, i+1, j+1))
                # add a symbol column
                temp['Symbol'] = ticker 
                symbols.append(temp)
                j += 1
    
            i += 1
			
    # concatenate all the dataframes
    df = pd.concat(symbols)
	
    cell= df[['Symbol','Open','High','Low','Adj Close','Volume']]
    cell.reset_index().sort_values(['Symbol', 'Date'], ascending=[1,1]).set_index('Symbol').to_csv(symbols_list[0]+'.csv', date_format='%d/%m/%Y')

    inFile = open(symbols_list[0]+'.csv', 'r')
    outFile =  open(symbols_list[0]+'Scraped'+'.csv', 'w')
    
    listLine = []
	
    for line in inFile:

        if line in listLine:
            continue
        else:
            outFile.write(line)
            listLine.append(line)
		
    outFile.close()
    inFile.close()
    os.remove(symbols_list[0]+'.csv')
		
    print "Finished writing"

	

	
	
