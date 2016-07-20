# Linear Regression for Stock based on Date 
# Currently only works for month
# http://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#example-linear-model-plot-ols-py

import csv
import numpy as np 
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt

close_prices = [] 
volumes = [] 

f = raw_input('Enter filename: \n')

if not(f.endswith('.csv')):
	f = f + '.csv'
	
with open(f, 'r') as file:
	the_data = csv.reader(file);
	the_data.next()
	
	for row in the_data:
		x = float(row[4])
		close_prices.append(float("{0:.2f}".format(x)))
		volumes.append(float(row[5]))

#convert lists to numpy arrays
prices_arr = np.reshape(close_prices, (len(close_prices), 1))
volumes_arr = np.reshape(volumes, (len(volumes), 1))


#Creating lin reg object
regr = linear_model.LinearRegression()
regr.fit(volumes_arr, prices_arr)

print 'Coefficients: '
print regr.coef_

# Explained variance score: 1 is perfect prediction
print 'Variance score: %.2f' % regr.score(volumes_arr, prices_arr)


minpr = min(close_prices)
maxpr = max(close_prices)
minv = min(volumes)
maxv = max(volumes)

#Draw black dots representing prices
plt.figure(figsize=(10,10), dpi=240)
plt.scatter(volumes_arr, prices_arr, color = 'black', label = 'Close Prices')
plt.plot(volumes_arr, regr.predict(volumes_arr), color = 'red', linewidth = 4, label = 'Estimated Linear Function')
plt.xlabel('Volume of Shares')
plt.ylabel('Close Price')
plt.title('Linear Regression')
plt.ylim([minpr - 3, maxpr + 3])
plt.xlim(minv - 1000, maxv + 1000)
plt.subplots_adjust(bottom=0.13)
plt.subplots_adjust(top=0.92)
plt.subplots_adjust(left=0.07)
plt.subplots_adjust(right=0.96)
plt.legend()
plt.show()