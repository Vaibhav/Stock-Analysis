import numpy as np
import pandas.io.data as pd 


def trendGen(xDat, window=1.0/3.0, charts=True): 
    
    x = np.array(xDat)
    xLen = len(x)
    window = window * xLen
    window = int(window)

    # find index of min and max
    absMax = np.where(x == max(x)[0][0]) 
    absMin = np.where(x == min(x)[0][0])

    if absMax + window > xLen:
        xmax = max(x[0:(absMax - window)])
    else:
        xmax = max(x[(absMax + window)])
        
    
    if absMin - window < 0:
        xmin = min(x[(absMin + window)])
    else:
        xmin = min(x[0:(absMin - window)])

