# Machine learning classification libraries
from sklearn.svm import SVC
from sklearn.metrics import scorer, accuracy_score

# For data manipulation
import pandas as pd
import numpy as np
from math import floor

# To plot
import matplotlib.pyplot as plt

# To fetch data
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime

# Fetch the data
ticker = "MSFT"
df = yf.Ticker(ticker).history(period="2y")
df= df.dropna()

# Create features
y = np.where(df['Close'].shift(-1) > df['Close'],1,-1)
df['Open-Close'] = df.Open - df.Close
df['High-Low'] = df.High - df.Low

x=df[['Open-Close','High-Low', 'High', 'Low', 'Volume']]

split_percentage = 0.75
split = int(floor(split_percentage*len(df)))

# Train data set
x_train = x[:split]
y_train = y[:split]

# Test data set
x_test = x[split:]
y_test = y[split:]

cls = SVC().fit(x_train, y_train)

accuracy_train = accuracy_score(y_train, cls.predict(x_train))
accuracy_test = accuracy_score(y_test, cls.predict(x_test))

print('Train Accuracy:{: .2f}%'.format(accuracy_train*100))
print('Test Accuracy:{: .2f}%'.format(accuracy_test*100))

df['Predicted_Signal'] = cls.predict(x)

# Calculate returns
lag_price = df.Close.shift(1)

df['Return'] = (df.Close - lag_price) / lag_price
df['Strategy_Return'] = df.Return * df.Predicted_Signal.shift(1)

# Plot results

df.Strategy_Return.iloc[split:].cumsum().plot(figsize=(10,5))  # Strategy returns
plt.plot(df.Return.iloc[split:].cumsum()) # buy and hold
plt.ylabel("Strategy Returns (%)")
plt.show()

# print(df)
