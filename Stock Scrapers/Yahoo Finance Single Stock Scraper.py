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
import shutil
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

#Asks user to input starting year 
year = raw_input('Enter starting year: \n')
the_year = year.strip()
year = year.strip()

#Ask user if they want ascending order or descending order
print 'Enter 1 if you want the oldest prices at the top. \n'
asc = raw_input('Enter 0 if you want the most recent prices at the top: \n')
asc = int(asc)
now = datetime.datetime.now()
f = symbols_list[0] + '-Scraped_' + str(now.hour) + '-' + str(now.minute) + '.csv';

if os.path.isfile(f) == False:

    symbols=[]
    #fix for bug when user inserts current year as starting year
    is_today = 0;
    year = int(year)

    if(year == now.year):
        year = year - 1
        is_today = 1;

    #Getting the Data for each day
    for ticker in symbols_list:
        print ticker
        i,j = 0,0
        
        for i in range (0,month):
            print months[i]
				
            for j in range(0,business_days):
				
                print j+1
                
                #Use Yahoo Finance API to retrive stock data for given day and month
                temp = dr.DataReader(ticker, "yahoo", start=datetime.datetime(year, i+1, j+1))
               
                temp['Symbol'] = ticker 
                symbols.append(temp)
                j += 1
    
            i += 1
			
    df = pd.concat(symbols)
	
    cell= df[['Open','High','Low','Close','Volume']]
    cell.reset_index().sort_values(['Date'], ascending=[asc]).set_index('Date').to_csv(symbols_list[0]+'.csv', date_format='%d/%m/%Y')

    
    #Naming Files
    inFile = open(symbols_list[0]+'.csv', 'r')
    outFile =  open(f, 'w')

    #Removing Duplicates and implementation for bug fix
    listLine = []
    the_year = '/' + the_year
    
    for line in inFile:

        #Keep the first line
        if line.startswith('Date'):
            outFile.write(line)
        
        if line in listLine:
            continue;
        
        if is_today == 1 and the_year not in line:
            continue;

        if first_row == 1:
            first_row = 0
            continue;
        
        else:
            outFile.write(line)
            listLine.append(line)
		
    outFile.close()
    inFile.close()
    os.remove(symbols_list[0]+'.csv')

    #Saves file in Datasets folder
    shutil.move(f, "Datasets/")
    print "Finished writing - Check Datasets Folder"
	
######################################################
