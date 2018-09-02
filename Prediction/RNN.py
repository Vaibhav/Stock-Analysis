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
stockNames = "SPY"
target = .01     # Target to identify if stock increased by 1%
window = 5       # Window to identify whether stock hit target within these number of days
p = 120          # number of days of data for each data point

# Inital 5 data inputs
features = ["open_high", "open_low", "open_close", "close_open", "close_close"]

# Load the OHLC data into the variable data
data_source = 'iex'
start_date = datetime(2013, 1, 1)
end_date = datetime(2018, 8, 31)

# Measure how long it takes to load the data
startTime = time.time()

# Load the data
stock_data = data.DataReader(stockNames, data_source, start_date, end_date)
column_labels = stock_data.columns

print(stock_data.head())

print("Loading data for {} stocks took {:3.1f} seconds".format(len(stockNames), time.time()-startTime))

# Sort the data by date so that we can reference slices of the date index later
stock_data.sort_index(level=[0], axis=0, inplace=True)

print("===========Summary===========")
print(stock_data.describe())


def add_ma(data):
  data['10dma'] = data['close'].rolling(window=10, min_periods=10).mean()
  data['20dma'] = data['close'].rolling(window=20, min_periods=10).mean()
  data['50dma'] = data['close'].rolling(window=50, min_periods=10).mean()
  return data


def get_trading_days(data):
    return data.shape[0]


def create_is_sellable_flag(data, window = 5, target = 0.01):
    # Identify the stocks within the data
    # stockNames = data.index.levels[0].values

    # Identify the number of trading days uploaded for each stock
    trading_days = get_trading_days(data)
    print("=======Trading Days=======")
    print(trading_days)

    open_price = data.open
    high = data.high

    # Create a `is_sellable` flag column filled with 0s
    is_sellable = pd.Series(0, index=data.index, name="is_sellable")

    startTime = time.time()

    #TODO: Vectorize this part. It takes a long time to run.
    # For loop to add the column with flags to identify if stock will hit target within window
    for stock in stockNames:
        index = 0
        for indexDate in data.loc[stock].index:
            endIndex = min(index + window, trading_days[stock]-1)

            # We take the endIndex - 1 because when slicing the dates
            # for high_window below, the slice takes both the start and end times inclusive.
            endDate = data.loc[stock].index[endIndex-1]
            high_window = high.loc[stock,indexDate:endDate]

            # If high price within the high_window is greater than target price, set is_sellable to 1
            if (high_window > open_price.loc[stock,indexDate] * (1+target)).any():
                is_sellable.loc[stock, indexDate] = 1
            index += 1

    # Add is_sellable column to the data variable
    print("Creating is_sellable column took {:3.1f} seconds".format(time.time()-startTime))
    data = pd.concat((data, is_sellable), axis=1)

    return data


stock_data = add_ma(stock_data)
print(stock_data.head(100))

# stock_data = create_is_sellable_flag(stock_data, window=window, target=target)









