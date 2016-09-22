import requests
import time
import ast
import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import math

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(this):
    ax1.clear()
    full_trades = get('trades')
    depth = get('depth')
    price = full_trades[0]['price']
    asks, bids = get_depth_data(depth, norm=False)
    asks = np.transpose(asks)
    bids = np.transpose(bids)
    #ax1.set_ylim([-.5,25])
    #ax1.set_xlim([586,587.5])

    ax1.scatter(bids[0], bids[1], color='green')
    ax1.scatter(asks[0], asks[1], color='red')
    for i in range(1):
        price = full_trades[i]['price']
        amount = full_trades[i]['amount']
        ttype = full_trades[i]['type']
        if ttype == 'bid':
            ax1.scatter(price, amount, s=50, color='red')
            ax1.scatter(price, amount, s=30, color='black')
        else:
            ax1.scatter(price, amount, s=50, color='green')
            ax1.scatter(price, amount, s=30, color='black')


def get(method, seconds=2, variation=1):
    try:
        r = requests.get('https://btc-e.com/api/3/' + method + '/btc_usd/')
        # wait(seconds, variation)
        return ast.literal_eval(r.text)['btc_usd']
    except Exception as e:
        print(str(e))


def get_depth_data(depth, price=None, norm=False):
    # Create/Format relevant depth data
    asks = depth['asks']
    bids = depth['bids']

    if price is not None:
        for i in range(len(asks)):
            asks[i][0] = (asks[i][0]-price)/price
        for i in range(len(bids)):
            bids[i][0] = (bids[i][0]-price)/price

    if norm:
        for ask in asks:
            ask[1] = math.log(ask[1])
        for bid in bids:
            bid[1] = math.log(bid[1])
    return asks, bids

ani = animation.FuncAnimation(fig, animate, interval=2000)
plt.show()
