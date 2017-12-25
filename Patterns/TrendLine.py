import numpy as np
import pandas.io.data as pd 


def trendGen(xDat, window=1.0/3.0, charts=True): 
    
    x = np.array(xDat)

    window = window * len(x)
    window = int(window)

    
