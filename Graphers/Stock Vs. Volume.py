
import csv
import matplotlib.pyplot as plt
import numpy as np


#1346518700

f = open('AMZNScraped.csv')
stock = csv.reader(f)
stock.next()

close_prices = []
volume = []

for row in stock:
		x = float(row[5])
		close_prices.append(float("{0:.2f}".format(x)))
		volume.append(float(row[6]) / 100000)
	
plt.plot(close_prices, '.r-')
plt.plot(volume, 'b:')
plt.title("AMZN")
plt.subplots_adjust(bottom=0.13)
plt.subplots_adjust(top=0.92)
plt.subplots_adjust(left=0.07)
plt.subplots_adjust(right=0.96)
plt.xticks([w*20 for w in range(50)], 
  ['Month %i'%w for w in range(50)])
plt.xticks(rotation=90)
plt.autoscale(enable=True, axis='both')
plt.grid()
plt.show()

'''
r       Red
g	Green
b	Blue
c	Cyan
m	Magenta
y	Yellow
k       Black
w	White
'''
