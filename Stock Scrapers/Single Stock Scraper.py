##############
'''
   Author: Vaibhav Khaitan
   Date: July 2016
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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import DataFrame
from pandas_datareader import data as dr
from pyalgotrade.barfeed import yahoofeed
import fileinput

start = timeit.default_timer()
month = 12
business_days = 20
months =  ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']



def get_data(symbols_list, year, asc):

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
        tmp = [now, is_today]
        return tmp

def remove_dup(symbols_list, now, the_year, is_today):

    f = symbols_list[0] + '-Scraped_' + str(now.hour) + '-' + str(now.minute) + '.csv';
    #Naming Files
    #inFile = open(symbols_list[0]+'.csv', 'r')
    #outFile =  open(f, 'w')

    #Removing Duplicates and implementation for bug fix
    #listLine = []
    fileyear = str(the_year)
    
    the_year = '/' + the_year

    #seen = set() # set for fast O(1) amortized lookup

    toclean = pd.read_csv(symbols_list[0]+'.csv', header = None)
    deduped = toclean.drop_duplicates()
    deduped.to_csv(f)

    with open(f,"rb") as source:
        rdr = csv.reader(source)
        rdr.next()
        with open(symbols_list[0]+fileyear+'.csv',"wb") as result:
            wtr = csv.writer(result)
            for r in rdr:
                    wtr.writerow( (r[1], r[2], r[3], r[4], r[5], r[6]))
    
    '''
    for line in inFile:
        
        if line in seen:
            continue;
        
        if is_today == 1 and the_year not in seen:
            continue;

        #Keep the first line
        if line.startswith('Date'):
            outFile.write(line)
            seen.add(line)
            continue;
        
        else:
            outFile.write(line)
            seen.add(line)
    '''
    
    #outFile.close()
    #inFile.close()
    os.remove(symbols_list[0]+'.csv')
    os.remove(f)
    
    #Saves file in Datasets folder
    shutil.move(symbols_list[0]+fileyear+'.csv', "Datasets/")
    print "Finished writing - Check Datasets Folder"
	
######################################################



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

tempo = get_data(symbols_list, year, asc)
now = tempo[0]
is_today = tempo[1]

remove_dup(symbols_list, now, the_year, is_today)

stop = timeit.default_timer()

print stop - start
