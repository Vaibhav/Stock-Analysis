'''
Author: Vaibhav Khaitan
Date: 8/17/2018
Description: Creates a dataframe with moving averages and MACD oscillator
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from iexfinance import get_historical_data

moving_avg1 = 10
moving_avg2 = 20
ticker = "BABA"

now = datetime.now()
start = now - timedelta(days=90)
df = get_historical_data(ticker, start=start, end=now, output_format='pandas')


def macd(dat):
  dat['10dma'] = dat['close'].rolling(window=moving_avg1, min_periods=1).mean()
  dat['20dma'] = dat['close'].rolling(window=moving_avg2, min_periods=1).mean()

  return dat


def add_macd(df):

  df = macd(df)
  df['position'] = 0

  df['position'][moving_avg1:] = np.where(df['10dma'][moving_avg1:] >= df['20dma'][moving_avg1:], 1, 0)

  df['signals'] = df['position'].diff()
  df['oscillator'] = df['10dma'] - df['20dma']

  return df


df = add_macd(df)
# print(df)
print(df.loc[df['signals'] == 1])
print(df.loc[df['signals'] == -1])
