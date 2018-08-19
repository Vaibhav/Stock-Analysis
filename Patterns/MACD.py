'''
Author: Vaibhav Khaitan
Date: 8/17/2018
Description:
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pandas_datareader import data
from iexfinance import Stock, get_historical_data, get_available_symbols

moving_avg1 = 10
moving_avg2 = 20
ticker = "BABA"

now = datetime.now()
start = now - timedelta(days=90)
df = get_historical_data(ticker, start=start, end=now, output_format='pandas')


def macd(dat):
  dat['ma1'] = dat['close'].rolling(window=moving_avg1, min_periods=1).mean()
  dat['ma2'] = dat['close'].rolling(window=moving_avg2, min_periods=1).mean()

  return dat


def add_macd(df):

  df = macd(df)
  df['position'] = 0

  df['position'][moving_avg1:] = np.where(df['ma1'][moving_avg1:] >= df['ma2'][moving_avg1:], 1, 0)

  df['signals'] = df['position'].diff()
  df['oscillator'] = df['ma1'] - df['ma2']

  return df


df = add_macd(df)
print(df)
