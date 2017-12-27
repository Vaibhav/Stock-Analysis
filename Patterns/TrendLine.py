import numpy as np
#import pandas.io.data as pd
from matplotlib.pyplot import plot, grid, show
from pandas_datareader import data, wb
import pandas as pd

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
        show()

    return trends, slopeMax, slopeMin


dat = data.DataReader("BABA", "yahoo")['Adj Close']

trendGen(dat, window = 1.0/3)
