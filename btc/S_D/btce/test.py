import requests
import time
from random import uniform
import ast
import math
import threading


# TODO send text messages for except blocks
# TODO implement threading


def main():
    server_time = 1470317709
    while True:

def wait(seconds, variation):
    rand = uniform(-variation, variation)
    time.sleep(seconds + rand)


def get(method, seconds=2, variation=1):
    try:
        r = requests.get('https://btc-e.com/api/3/'+method+'/btc_usd/')
        # wait(seconds, variation)
        return ast.literal_eval(r.text)['btc_usd']
    except Exception as e:
        print(str(e))


def get_depth_data(depth, price=None):
    # Create/Format relevant depth data
    asks = depth['asks']
    bids = depth['bids']
    if price is not None:
        # Reformat asks
        for ask in asks:
            ask[0] = 100. * (ask[0] - price) / price
            ask[1] = math.log(ask[1])

        # Reformat bids
        for bid in bids:
            bid[0] = 100. * (bid[0] - price) / price
            bid[1] = math.log(bid[1])
        return asks, bids
    else:
        return asks, bids

main()
