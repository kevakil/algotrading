import time
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

num = 500000
n = 500
val = 50
var = 25


def test_data():
    dates = []
    prices = []
    volumes = []
    try:
        source = open('/home/keyan/fun/algotrading/btc/coinbaseUSD.csv','r').read()
        split_source = source.split('\n')
        for line in split_source[-num:]:
            split_line = line.split(',')
            dates.append(float(split_line[0]))
            prices.append(float(split_line[1]))
            volumes.append(float(split_line[2]))
    except Exception as e:
        print('failed to open data file', str(e))

    ax1 = plt.subplot2grid((6, 4), (2, 0), rowspan=4, colspan=4)
    ax1.plot(dates, prices)
    ax1.grid(True)

    ax2 = plt.subplot2grid((6, 4), (0, 0), sharex=ax1, rowspan=2, colspan=4)
    rsiLine = calc_rsi(prices, n=n)
    ax2.plot(dates, rsiLine)
    ax2.axhline(val+var, color='r')
    ax2.axhline(val-var, color='g')
    ax2.set_yticks([val-var, val+var])
    ax2.grid(True)

    plt.show()


def calc_rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1]  # since the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0
        else:
            upval = 0
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100.-100./(1.+rs)

    return rsi


def ema(values, window):
    weights = np.exp(np.linspace(-1.,0.,window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def backtest():
    dates = []
    prices = []
    volumes = []
    try:
        source = open('/home/keyan/fun/algotrading/btc/coinbaseUSD.csv','r').read()
        split_source = source.split('\n')
        for line in split_source[-num:]:
            split_line = line.split(',')
            dates.append(float(split_line[0]))
            prices.append(float(split_line[1]))
            volumes.append(float(split_line[2]))

    except Exception as e:
        print('failed to open data file', str(e))

    EMA_prices = ema(prices, 50)
    rsi_values = calc_rsi(EMA_prices, n=n)

    x = 0
    stance = 'none'
    last_bought_for = 0
    profit = 0
    print 'starting time', str(datetime.datetime.fromtimestamp(float(dates[0])).strftime('%Y-%m-%d %H:%M:%S'))
    while x < len(rsi_values):
        if stance == 'none':
            if rsi_values[x] < val - var:
                stance = 'holding'
                print 'Buying BTC @', prices[x]
                last_bought_for = prices[x]
        elif stance == 'holding':
            if rsi_values[x] > val+var:
                stance = 'none'
                print 'Selling BTC @', prices[x]
                fees = 0
                fees = (.002)*(prices[x]+last_bought_for)
                print 'Fee was ', fees
                print 'Profit on this trade:', prices[x]-last_bought_for-fees
                profit += (prices[x]-last_bought_for-fees)
        x += 1
    print('Total profit: ' + str(profit))

# test_data()
backtest()
