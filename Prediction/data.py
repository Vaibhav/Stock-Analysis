# Machine learning classification libraries
from sklearn.svm import SVC
from sklearn.metrics import scorer
from sklearn.metrics import accuracy_score

# For data manipulation
import pandas as pd
import numpy as np

# To plot
import matplotlib.pyplot as plt

# To fetch data
from pandas_datareader import data as pdr
from iexfinance import get_historical_data
from datetime import datetime

# Fetch the data
ticker = "AAPL"
start = datetime(2015,1,1)
now = datetime.now()

df = get_historical_data(ticker, start=start, end=now, output_format='pandas')
df= df.dropna()

y = np.where(df['close'].shift(-1) > df['close'],-1,1)
df['Open-Close'] = df.open - df.close
df['High-Low'] = df.high - df.low

x=df[['Open-Close','High-Low']]

split_percentage = 0.8
split = int(split_percentage*len(df))

# Train data set
x_train = x[:split]
y_train = y[:split]

# Test data set
x_test = x[split:]
y_test = y[split:]

cls = SVC().fit(x_train, y_train)

accuracy_train = accuracy_score(y_train, cls.predict(x_train))
accuracy_test = accuracy_score(y_test, cls.predict(x_test))

print('\nTrain Accuracy:{: .2f}%'.format(accuracy_train*100))
print('Test Accuracy:{: .2f}%'.format(accuracy_test*100))

df['Predicted_Signal'] = cls.predict(x)

# Calculate log returns
df['Return'] = np.log(df.close.shift(-1) / df.close)*100
df['Strategy_Return'] = df.Return * df.Predicted_Signal
df.Strategy_Return.iloc[split:].cumsum().plot(figsize=(10,5))
plt.ylabel("Strategy Returns (%)")
plt.show()

print(df)
