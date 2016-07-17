# Linear Regression for Stock based on Date 
# Currently only works for month
# http://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#example-linear-model-plot-ols-py

import csv
import numpy as np 
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt

close_prices = []
dates = [] 

f = raw_input('Enter filename: \n')

if not(f.endswith('.csv')):
	f = f + '.csv'
	
with open(f, 'r') as file:
	the_data = csv.reader(file);
	the_data.next()
	
	for row in the_data:
		x = float(row[4])
		close_prices.append(float("{0:.2f}".format(x)))
		dates.append(int(row[0].split('/')[0]))

#convert lists to numpy arrays
prices_arr = np.reshape(close_prices, (len(close_prices), 1))
dates_arr = np.reshape(dates, (len(dates), 1))


#Creating lin reg object
regr = linear_model.LinearRegression()
regr.fit(dates_arr, prices_arr)

print 'Coefficients: '
print regr.coef_

# Explained variance score: 1 is perfect prediction
print 'Variance score: %.2f' % regr.score(dates_arr, prices_arr)

#Draw black dots representing prices
plt.scatter(dates_arr, prices_arr, color = 'black', label = 'Close Prices')
plt.plot(dates_arr, regr.predict(dates_arr), color = 'red', linewidth = 4, label = 'Estimated Linear Function')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Linear Regression')
plt.subplots_adjust(bottom=0.13)
plt.subplots_adjust(top=0.92)
plt.subplots_adjust(left=0.07)
plt.subplots_adjust(right=0.96)
plt.legend()
plt.show()
