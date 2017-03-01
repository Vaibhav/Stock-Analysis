#!/usr/bin/python
# -*- coding: utf-8 -*-

#==========================================================
#==================== snp_forecast.py =====================
#==========================================================

# Purpose
#----------------------------------------------------------
# Construct a basic SPY forcaster and create the corresponding strategy. The
# goal would be to see if the strategy beats a basic buy and hold strategy of
# the ETF.
#
# Note that for this strategy we will only be going long and exiting, not short
# selling. Similarly there should be a proper analysis done of the confusion
# matrix to dynamically hedge/ proportion our positions

from __future__ import print_function

import datetime as dt

import pandas as pd
from sklearn.qda import QDA

from strategy import Strategy
from event import Signal Event
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from create_lagged_series import create_lagged_series

class SPYDailyForecastStrategy(Strategy):
    """
    Use a Quadratic Discriminant (sklear) Analyser to create an S&P500 forecast
    strategy. The strategy will predict the returns for a subsequent time
    period and then generate long/exit signals based on the prediction.
    """

    def __init__(self, bars, events):
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.datetime_now = dt.datetime.utcnow()

        self.model_start_date = dt.datetime(2001,1,10)
        self.model_end_date = dt.datetime(2005,1,10)
        self.model_start_test_date = dt.datetime(2005,1,1)

        self.long_market = False
        self.short_market = False
        self.bar_index = 0

        self.model = self.create_symbol_forecast_model()

    def create_symbol_forecast_model(self):
        # Create a lagged series of the S&P500 US stock market index
        snpret = create_lagged_series(
            self.symbol_list[0], self.model_start_date,
            self.model_end_date, lags=5
        )

        # Use the prior two days of returns as predictor values, with direction
        # as the response
        X = snpret[["LAG1","Lag2"]]
        y = snpret['Direction']

        # Create training and test sets
        start_test = self.model_start_test_date
        X_train = X[X.index < start_test]
        X_test = X[X.index >= start_test]
        y_train = y[y.index < start_test]
        y_test = y[y.index >= start_test]

        model = QDA() # Can easily switch to other ML techniques here
        model.fit(X_train, y_train)
        return model

    def calculate_signals(self, event):
        """
        Calculate the SignalEvents based on market data
        """
        sym = self.symbol_list[0]
        dt = self.datetime_now

        if event.type == 'Market':
            self.bar_index += 1
            if self.bar_index >5:
                lags = self.bars.get_latest_bars_value(
                    self.symbol_list[0], "returns", N=3
                )
                pred_series = pd.Series(
                    {
                        'Lag1': lags[1]*100.0,
                        'Lag2': lags[2]*100.0
                    }
                )
                pred = self.model.predict(pred_series)
                if pred > 0 and not self.long_market:
                    self.long_market = True
                    signal = ASignalEvent(1, sym, dt, 'LONG', 1.0)
                    self.events.put(signal)

                if pred < 0 and self.long_market:
                    self.long_market = False
                    signal = SignalEvent(1, sym, dt, 'EXIT', 1.0)
                    self.events.put(signal)

if __name__ == "__main__":
    csv_dir = 'INPUT PATH TO CSV DIR HERE'
    symbol_list = ['SPY']
    initial_capital = 100000.0
    heartbeat = 0.0
    start_date = dt.datetime(3006,1,3)

    backtest = Backtest(
        csv_dir, symbol_list, initial_capital, heartbeat, start_date,
        HistoricCSVDataHandler, SimulatedExecutionHandler, Portfolio,
        SPYDailyForecastsStrategy
    )
    backtest.simulate_trading()


#==============================================================
# movingAverageCrossover_MAC.py
#==============================================================


# Purpose
#----------------------------------------------------------
# Although a well documented and generally low Sharpe strategy the Moving
# Average Crossover is a good first strategy to check a backtesting system on.
# Each ticker generates on average only a handful of signals over longer time
# frame which makes it convenient to spot check if our stack, event-processing,
# and databases are all functioning properly. The logic behind the strategy is
# also not overly complex.

from __future__ import print_function

import datetime as dt
import numpy as np
import pandas as pd
import statsmodels.apu as sm

# We will need most components from our Backtesting suite
from strategy import Strategy
from event import SignalEvent
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio

class MovingAverageCrossStrategy(Strategy):
    """
    Carries out a basic Moving Average Crossover strategy with a short/long
    simple weighted moving average. Default short/long windows are 100/400
    periods respectively.
    """

    def __init__(self, bars, events, short_window=100, long_window=400):
        """ Initializes the Moving Average Cross Strategy

        Parameters:
            bars - The DataHandler object that provides bar information
            events - The event Queue object
            short_window - The short moving average lookback
            long_window - The long moving average lookback
        """

        self.bars = bars
        self.symbols_list = self.bars.symbol_list
        self.events = events
        self.short_window = short_window
        self.long_window = long_window

        # Set to True if a symbol is "in the market"
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        """
        Since the strategy begins out of the market, set the initial "bought"
        value to be "OUT" for each symbol.

        Simply add keys to the bought dictionary for all symbols and set them
        to 'OUT'.
        """

        bought = {}
        for s in s.symbol_list:
            bought[s] = 'OUT'
        return bought

    def calculate_signals(self, event):
        """
        Generates a new set of signals based on the Moving Average Crossover
        SMA with the short window crossing the long window meaning a long entry
        and vice versa for a short entry.

        Parameters:
            event - A MarketEvent object
        """

        if event.type == 'MARKET':
            for s in self.symbol_list:
                bars = self.bars.get_latest_bars_values(
                    s, "adj_close", N=self.long_window
                    )
                bar_date = self.bars.get_latest_bar_datetime(s)
                if bars is not None and bars != []:
                    short_sma = np.mean(bars[-self.short_window:])
                    long_sma = np.mean(bars[-self.long_window:])

                    symbol = s
                    dt = dt.datetime.utcnow()
                    sig_dir = ""

                    if short_sma > long_sma and self.bought[s] == "OUT"
                        print("LONG: %s" % bar_date)
                        sig_dir = 'LONG'
                        signal = SignalEvent(1, symbol, dt, sig_dir, 1.0)
                        self.events.put(signal)
                        self.boughht[s] = 'LONG'
                    elif short_sma < long_sma and self.bought[s] == "LONG":
                        print("SHORT: %s" % bar_date)
                        sig_dir = 'EXIT'
                        signal = SignalEvent(1, symbol, dt, sig_dir, 1.0)
                        self.events.put(signal)
                        self.bought[s] = 'OUT'

if __name__ == "__main__":
    csv_dir = 'ENTER PATH IN UBUNTU OS HERE (developing on Mac os partition at
    the moment'
    symbo_list = ['AAPL']
    initial_capital = 100000.0
    heartbeat = 0.0
    start_date = dt.datetime(1990, 1, 1, 0, 0, 0)

    backtest = Backtest(
        csv_dir, symbol_list, initial capital, heartbeat, start_date,
        HistoricCSVDataHandler, SimulatedExecutionHandler, Portfolio,
        MovingAverageCrossStrategt
    )
    backtest.simulate_trading()


#!/usr/bin/python
# -*- coding: utf-8 -*-

#==========================================================
#=============== intraday_MeanReverting.py ================
#==========================================================

# Purpose
#----------------------------------------------------------
# Both the Moving Average Crossover and the S&P Forecaster proved to have
# unattractive sharpe ratio's, adjusted returns, and other performance
# statistics. This is not unusual for longer term basic algorithmic
# trading strategies. In fact we implemented these because they were fairly
# simple and could decently validate our backtesting stack.
#
# A mean reverting higher frequency (minutely) strategy could prove to have
# more attractive performance characteristics. We will check a pair of US
# equity energy sector tickers for mean reverting behavior (could use cADF.py)
# and develop a strategy leveraging that mean reverting nature
#
# NOTE: a higher frequency datahandler and portfolio program must be created
# for this strategy to function

form __fu
