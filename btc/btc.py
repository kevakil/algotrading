import time
import json
import urllib2
from matplotlib import pyplot as plt

def main():
	btcePrices = urllib2.urlopen('https://btc-e.com/api/2/btc_usd/ticker').read()
	btcejson = json.loads(btcePrices)
	btcelastP = btcejson['ticker']['last']
	btcelastT = btcejson['ticker']['updated']

	return btcelastP, btcelastT

prices = []
times = []
curr = time.time()

while time.time() > curr + 30:
	price, time = main()
	prices.append(price)
	times.append(time)
	time.sleep(1)

plt.plot(prices, times)
