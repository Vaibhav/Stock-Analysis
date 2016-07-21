# Linear Regression for Stock based on Date 
# Currently only works for month
# http://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#example-linear-model-plot-ols-py

import csv
import numpy as np 
from sklearn import datasets, linear_model
from sklearn.svm import SVR
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
day.reverse()

prices_arr = np.reshape(close_prices, (len(close_prices), 1))
days_arr = np.reshape(day, (len(day), 1))

# days_arr = np.reshape(dates, (len(dates), 1))

print '0'
# Fit regression model
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
print '1'
svr_rbf.fit(days_arr, close_prices)
svr_lin.fit(days_arr, close_prices)
svr_poly.fit(days_arr, close_prices)

predict_num = day[0] + 1

print "RBF = " + str(svr_rbf.predict(predict_num))
print "Lin = " + str(svr_lin.predict(predict_num))
print "Poly = " + str(svr_poly.predict(predict_num))

minpr = min(close_prices)
maxpr = max(close_prices)

maxdt = predict_num
mindt = 1

#Draw black dots representing prices
plt.figure(figsize=(15,15), dpi=240)
plt.scatter(days_arr, prices_arr, color = 'black', label = 'Close Prices')

plt.plot(days_arr, svr_lin.predict(days_arr), color = 'blue', linewidth = 3, label = 'Linear Model')
plt.plot(days_arr, svr_poly.predict(days_arr), color = 'green', linewidth = 3, label = 'Polynomial Model')
plt.plot(days_arr, svr_rbf.predict(days_arr), color = 'red', linewidth = 4, label = 'RBF Model')

plt.xlabel('Day')
plt.ylabel('Close Prices')
plt.title('SVR Model')
plt.ylim([minpr - 3, maxpr + 3])
plt.xlim([mindt - 1, maxdt + 5])
plt.subplots_adjust(bottom=0.13)
plt.subplots_adjust(top=0.92)
plt.subplots_adjust(left=0.07)
plt.subplots_adjust(right=0.96)
plt.legend()
plt.show()

#742.95
