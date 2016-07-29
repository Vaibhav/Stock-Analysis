#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import csv

def get_data(f, close_prices, dates):

    if not(f.endswith('.csv')):
        f = f + '.csv'

    with open(f, 'r') as file:
        the_data = csv.reader(file);
        #Skip the row with headers
        the_data.next()

        for row in the_data:
            #convert close price to float
            x = float(row[4])
            #convert close price to a price (2 decimal points)
            close_prices.append(float("{0:.2f}".format(x)))
            dates.append(int(row[0].split('/')[0]))
            
    length_of_dates = len(dates)
    days = []
    days.extend(range(1, length_of_dates+1))
    
    return days, close_prices
            
def linear_regression(x, y):
    length_of_x = len(x)
    sum_of_x = sum(x)
    sum_of_y = sum(y)

    sum_of_x_squared = sum(map(lambda m: m * m, x))
    
    sum_of_products = sum([x[i] * y[i] for i in range(0,length_of_x)])

    m = (sum_of_products - (sum_of_x * sum_of_y) / length_of_x) / (sum_of_x_squared - ((sum_of_x ** 2) / length_of_x))
    b = (sum_of_y - m * sum_of_x) / length_of_x
    tmp = [m, b]
    return tmp


close_prices = []
dates = []
f = raw_input('Enter filename: \n')
x,y = get_data(f, close_prices, dates)

rev = raw_input('Is the newest price first? (y/n)')
if rev.startswith('y'): y.reverse();
temp = linear_regression(x,y)

maxx = max(x)
maxy = max(y)
miny = min(y)

print temp
m = float(temp[0])
b = float(temp[1])

# Predict next day price based on linear line
# y = mx + b

print ((m * (maxx + 1)) + b)

pl.figure(figsize=(7,5), dpi=120)
pl.scatter(x, y, color = 'black', label = 'Close Prices')
pl.plot(x,m*np.asarray(x) + b, color = 'red', linewidth =  4, label = "Linear Regression Model")
pl.xlabel('Day')
pl.ylabel('Close Price')
pl.title('Linear Regression')
pl.xlim([0, maxx + 1])
pl.ylim([miny - 5, maxy + 5])
pl.grid()
pl.legend()
pl.show()
