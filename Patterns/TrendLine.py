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

today = datetime.now()
d = timedelta(days=365)
start = today - d
dat = data.DataReader("BABA", "iex", start, today)['close']

trendGen(dat, window = 1.0/3)


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


findTops(dat, window = 1.0/3)
