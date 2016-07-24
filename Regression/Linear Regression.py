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
length_of_dates = len(dates) + 1;
day = []
day.extend(range(1, length_of_dates))
close_prices.reverse()
prices_arr = np.reshape(close_prices, (len(close_prices), 1))
days_arr = np.reshape(day, (len(day), 1))

print close_prices
print day

#Creating lin reg object
regr = linear_model.LinearRegression()
regr.fit(days_arr, prices_arr)

print 'Coefficients: '
print regr.coef_

# Explained variance score: 1 is perfect prediction
print 'Variance score: %.2f' % regr.score(days_arr, prices_arr)


minpr = min(close_prices)
maxpr = max(close_prices)

maxdt = max(day)
mindt = min(day)

#Draw black dots representing prices
plt.figure(figsize=(15,15), dpi=240)
plt.scatter(days_arr, prices_arr, color = 'black', label = 'Close Prices')
plt.plot(days_arr, regr.predict(days_arr), color = 'red', linewidth = 4, label = 'Estimated Linear Function')
plt.xlabel('Day')
plt.ylabel('Close Price')
plt.title('Linear Regression')
plt.ylim([minpr - 3, maxpr + 3])
plt.xlim([mindt - 1, maxdt + 5])
plt.subplots_adjust(bottom=0.13)
plt.subplots_adjust(top=0.92)
plt.subplots_adjust(left=0.07)
plt.subplots_adjust(right=0.96)
plt.legend()
plt.show()


