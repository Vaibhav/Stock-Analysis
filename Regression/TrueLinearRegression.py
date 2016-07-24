import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import csv


def linear_regression(x, y):
    # Basic computations to save a little time.
    length_of_x = len(x)
    sum_x = sum(x)
    sum_y = sum(y)

    # Σx^2, and Σxy respectively.
    sum_x_squared = sum(map(lambda m: m * m, x))
    
    sum_of_products = sum([x[i] * y[i] for i in range(length_of_x)])

    m = (sum_of_products - (sum_x * sum_y) / length_of_x) / (sum_x_squared - ((sum_x ** 2) / length_of_x))
    b = (sum_y - m * sum_x) / length_of_x
    tmp = [m, b]
    return tmp


y = [53.52, 52.97, 52.7, 53.32, 52.78, 52.8, 52.02, 50.85, 48.89, 47.65, 47.35, 46.66, 47.01, 46.65, 45.9, 45.24, 45.73, 48.49, 47.23, 47.27, 47.56, 46.72, 47.55, 47.36, 46.88, 46.79, 46.2, 47.38, 46.18, 46.33, 46.24, 46.48, 47.14, 46.81]
x = range(0, 34)

y.reverse()

temp = linear_regression(x, y)

print temp
m = float(temp[0])
b = float(temp[1])

pl.scatter(x, y, color = 'black', label = 'Close Prices')
pl.plot(x,m*np.asarray(x) + b)
pl.grid()
pl.show()
