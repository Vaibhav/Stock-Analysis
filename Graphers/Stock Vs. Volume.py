
import csv
import matplotlib.pyplot as plt
import numpy as np


months =  ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
           'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
           'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
           'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
           'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',]


#1346518700

print "Make sure scraped data file is in the same directory as this script"

filename = raw_input('\nEnter name of file with scraped data: \n')
nos = raw_input('Enter name of stock: \n')

if filename.endswith('.csv'):
    print '\n'
else:
    filename = filename + '.csv'

f = open(filename)
stock = csv.reader(f)
stock.next()

close_prices = []
volume = []

for row in stock:

    x = float(row[4])
    close_prices.append(float("{0:.2f}".format(x)))
    volume.append(float(row[5]) / 100000)

plt.plot(close_prices, '.r-')
plt.plot(volume, 'b:')
plt.title(nos)
plt.subplots_adjust(bottom=0.13)
plt.subplots_adjust(top=0.92)
plt.subplots_adjust(left=0.07)
plt.subplots_adjust(right=0.96)

plt.xticks([w*20 for w in range(50)],
  [months[w] for w in range(50)])
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

'''
    if factor_found == 0:
        factor_found = 1;
        if row[5] > 999:
            length = len(row[5])
            length = length - 3;
            if row[4] < 100:
                length += 1;
            factor = 10 ** length
    '''
