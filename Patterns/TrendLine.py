## Requires Python 3

import numpy as np
from matplotlib.pyplot import plot, grid, show
from pandas_datareader import data, wb
import pandas as pd
from datetime import datetime, timedelta

def trendGen(xDat, window=1.0/3.0, needPlot=True):

    x = np.array(xDat)
    xLen = len(x)
    window = window * xLen
    window = int(window)

    # find index of min and max
    absMax = np.where(x == max(x))[0][0]
    absMin = np.where(x == min(x))[0][0]

    if absMax + window > xLen:
        xmax = max(x[0:(absMax - window)])
    else:
        xmax = max(x[(absMax + window):])


    if absMin - window < 0:
        xmin = min(x[(absMin + window):])
    else:
        xmin = min(x[0:(absMin - window)])

    xmax = np.where(x == xmax)[0][0]  # index of the 2nd max
    xmin = np.where(x == xmin)[0][0]  # index of the 2nd min

    # Create the trend lines
    # rise over run
    slopeMax = (x[absMax] - x[xmax]) / (absMax - xmax)
    slopeMin = (x[absMin] - x[xmin]) / (absMin - xmin)
    amax     = x[absMax] - (slopeMax * absMax)
    amin     = x[absMin] - (slopeMin * absMin)
    bmax     = x[absMax] + (slopeMax * (xLen - absMax))
    bmin     = x[absMin] + (slopeMax * (xLen - absMin))
    maxline  = np.linspace(amax, bmax, xLen)
    minline  = np.linspace(amin, bmin, xLen)

    trends = np.transpose(np.array((x, maxline, minline)))

    trends = pd.DataFrame(trends, index=np.arange(0, len(x)),
                          columns=['Data', 'Resistance', 'Support'])

    if needPlot:
        plot(trends)
        grid()
        show()

    return trends, slopeMax, slopeMin


def findTops(x, window=1.0/3, charts=True):

    x = np.array(x)
    xLen = len(x)

    if window < 1:
        window = int(window * xLen)

    sigs = np.zeros(xLen, dtype=float)

    i = window

    while i != xLen:
        if x[i] > max(x[i-window:i]): sigs[i] = 1
        elif x[i] < min(x[i-window:i]): sigs[i] = -1
        i += 1

    xmin = np.where(sigs == -1.0)[0]
    xmax = np.where(sigs == 1.0)[0]

    ymin = x[xmin]
    ymax = x[xmax]

    if charts is True:
        plot(x)
        plot(xmin, ymin, 'ro')
        plot(xmax, ymax, 'go')
        show()

    return sigs

def trendSegments(x, segs=2, charts=True):
    y = np.array(x)

    # Implement trendlines
    segs = int(segs)
    maxima = np.ones(segs)
    minima = np.ones(segs)
    segsize = int(len(y)/segs)
    for i in range(1, segs+1):
        ind2 = i*segsize
        ind1 = ind2 - segsize
        maxima[i-1] = max(y[ind1:ind2])
        minima[i-1] = min(y[ind1:ind2])

    # Find the indexes of these maxima in the data
    x_maxima = np.ones(segs)
    x_minima = np.ones(segs)
    for i in range(0, segs):
        x_maxima[i] = np.where(y == maxima[i])[0][0]
        x_minima[i] = np.where(y == minima[i])[0][0]

    if charts:
        plot(y)
        grid()

    for i in range(0, segs-1):
        maxslope = (maxima[i+1] - maxima[i]) / (x_maxima[i+1] - x_maxima[i])
        a_max = maxima[i] - (maxslope * x_maxima[i])
        b_max = maxima[i] + (maxslope * (len(y) - x_maxima[i]))
        upperline = np.linspace(a_max, b_max, len(y))

        minslope = (minima[i+1] - minima[i]) / (x_minima[i+1] - x_minima[i])
        a_min = minima[i] - (minslope * x_minima[i])
        b_min = minima[i] + (minslope * (len(y) - x_minima[i]))
        lowerline = np.linspace(a_min, b_min, len(y))

        if charts:
            plot(upperline, 'g')
            plot(lowerline, 'm')

    if charts:
        show()

    # OUTPUT
    return x_maxima, maxima, x_minima, minima


today = datetime.now()
d = timedelta(days=365)
start = today - d
dat = data.DataReader("BABA", "iex", start, today)['close']

trendSegments(dat)
trendGen(dat)
findTops(dat)
