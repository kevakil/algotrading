import time
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import pandas as pd
import sys
import backtest

# "live trading algorithm"
# backtesting is irrelevant
# finding the METHOD is more important
# TRUE TEST IS FORWARD TEST
# ideally use log of data to normalize
# for this example we are just using percent change for simplicity
# more like the end is less similar than beginning

# current implementation: forward percent change from starting point
    # buildup should be more accurate
    # beginnning is more accurate

# TODO make end more accurate by using reverse percent change
    # from last percent change what was the reverse


# UNIX timestamp, price, volume
coinbase = '/home/keyan/fun/algotrading/btc/btceUSD.csv'
num = 100
n=5
def main():
    try:
        df = pd.DataFrame(get_raw_data())
    except Exception as e:
        print(str(e))

def get_raw_data():
    times = []
    prices = [0]
    volumes = []
    try:
        source = open(coinbase,'r').read()
        split_source = source.split('\n')
        for line in split_source[-num:]:
            split_line = line.split(',')
            times.append(float(split_line[0]))
            prices.append(float(split_line[1]))
            volumes.append(float(split_line[2]))
    except Exception as e:
        print('failed to open data file', str(e))
    rsi_vals = rsiFunc(prices, n=n)
    prices = np.diff(prices) / prices[:-1] * 100.
    rsi_vals = np.delete(rsi_vals, -1)
    return {'time':times, 'price_p_change':prices, 'volume':volumes,'rsi':rsi_vals}

    """
    fig = plt.figure(figsize=(10,7))
    ax1 = plt.subplot2grid((40,40),(0,0),rowspan=40,colspan=40)
    ax1_2 = ax1.twinx()
    ax1_2.plot(times, volumes, color='black')
    ax1.plot(times, prices)
    plt.subplots_adjust(bottom=.23)
    plt.grid(True)
    plt.show()"""


def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi


def movingaverage(values, window):
    weigths = np.repeat(1.0, window) / window
    smas = np.convolve(values, weigths, 'valid')
    return smas  # as a numpy array


def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(x, slow=26, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow


main()
