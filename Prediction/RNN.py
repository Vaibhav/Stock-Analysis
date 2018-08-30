from datetime import datetime
import time

import numpy as np
from numpy import array, argmax

import pandas as pd
from pandas_datareader import data
from pandas import DataFrame

import matplotlib.pyplot as plt
from matplotlib import style

# Set our hyperparameter variables
stockNames = ["MSFT"]
target = .01     # Target to identify if stock increased by 1%
window = 5       # Window to identify whether stock hit target within these number of days
p = 120          # number of days of data for each data point

# Inital 5 data inputs
features = ["open_high", "open_low", "open_close", "close_open", "close_close"]

# Load the OHLC data into the variable data
data_source = 'morningstar'
start_date = datetime(2012, 1, 1)
end_date = datetime(2018, 5, 2)

# Measure how long it takes to load the data 
startTime = time.time()

# Load the data
stock_data = data.DataReader("MSFT", data_source, start_date, end_date)
column_labels = stock_data.columns

stock_data.drop(stock_data.index[0], inplace=True)
print(stock_data.head())

print("Loading data for {} stocks took {:3.1f} seconds".format(len(stockNames), time.time()-startTime))

# Sort the data by date so that we can reference slices of the date index later
stock_data.sort_index(level=[0], axis=0, inplace=True)
