import requests
import time
from random import uniform
import ast
import math
import threading


# for use with btc-e
# TODO send text messages for except blocks
# TODO implement threading


def main():
    # ---CURRENT MODEL---
    #
    # GIVEN:
    #   B/A Spread
    #   Current Time
    #
    # PREDICT:
    #   Last Transaction Price
    #   Last Transaction Time
    #
    # -------------------

    # TODO maybe there is some obvious way so that i don't have to call get_depth_data more than once
    # TODO instead of using API, parse the webpage for up to date information
    # Initialize trades
    print 'Initializing...'
    while True:
        time.sleep(2)
        full_trades = get('trades')
        depth = get('depth')
        print full_trades
        prev_transac_times = [1+math.log(((time.time() - full_trades[0]['timestamp'])/full_trades[0]['timestamp'])*(10**8))]
        prev_transac_prices = [100.*(full_trades[1]['price'] - full_trades[0]['price'])/full_trades[0]['price']]

        asks, bids = get_depth_data(depth, full_trades[0]['price'])
        # TODO input initial values into machine learning algo

        prev_tid = full_trades[0]['tid']

    while True:
        print '...'
        times = []
        prices = []
        types = []
        amounts = []
        # get full data
        # get depth first so if a trade occurs, we can observe the circumstances under which it occurred
        # with a delay of how long it took to get the data
        request_time = time.time()
        depth = get('depth')
        full_trades = get('trades')
        reception_time = time.time() - request_time

        pre_calc_time = time.time()
        if full_trades[0]['tid'] != prev_tid:
            # get current time and price
            curr_time = time.time()

            # Create/Format trades data

            # Reformatted in this order so time and price would be most up to date
            # Based on when the change was detected
            for i in range(len(full_trades)):
                # Only add the trade data that changed from the last timeframe
                # base case to break out of loop if a new trade is found
                if full_trades[i]['tid'] == prev_tid:
                    prev_tid = full_trades[0]['tid']
                    break
                else:
                    # update price (will break if the price updates 1>=50 at a time)
                    price = full_trades[i+1]['price']
                    times.append(1+math.log(((curr_time - full_trades[i]['timestamp'])/full_trades[i]['timestamp'])*(10**8)))
                    prices.append(100.*(full_trades[i]['price']-price)/price)
                    print full_trades[i]['price'], price
                    types.append(full_trades[i]['type'] == 'ask')
                    amounts.append(math.log(full_trades[i]['amount']))
                # TODO add case for when all trades just happen to be >=150 new trades

            print times, prices, types, amounts

            asks, bids = get_depth_data(depth, price)

            # addded to ml after appending/reformatting data instead of on the spot since it is important to diminish
            # the discrepancy (could be amended upon implementation of threading)
            for i in range(len(times)):
                # TODO input ml for types, amounts, asks, and bids as X and times, prices as y
                # (same asks/bids for different transactions is technically incorrect)
                pass
        else:
            # No transactions were done
            pass


        calc_time = time.time() - pre_calc_time

        # print 'Reception time:\t' + str(reception_time)
        # print 'Calculation time:\t' + str(calc_time)


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
