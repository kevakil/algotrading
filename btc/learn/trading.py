import time
import urllib
import http.client as httplib
import hashlib
import hmac
import json
import matplotlib.pyplot as plt

API_KEY = 'PWQR7AN3-2KA3CT3V-2J638BUY-NA0KAHHS-PX9FKN2E'
API_SECRET = '3a2c117d4dbff3fbbe3e7c3c2f90eba3a769c0534894011c4dc57ab0bcd24a37'


# create wrappers
def get_depth(limit=None):
	# convert parms to url format
	parms = {
		"method": "depth",
		"pair": "btc_usd",
		"limit": limit
	}
	parms = urllib.urlencode(parms)
	# may add .parse()
	# hash api secret
	hashed = hmac.new(API_SECRET, digestmod=hashlib.sha512)
	# update parms
	hashed.update(parms)
	# create signature
	signature = hashed.hexdigest()

	# create the headers and key and sign elements to it
	headers = {"Content-type": "application/x-www-form-urlencoded",
			   "Key": API_KEY,
			   "Sign": signature}

	# establish a connection
	conn = httplib.HTTPSConnection("btc-e.com")
	conn.request("GET", "/api/3/depth/btc_usd", parms, headers)

	response = conn.getresponse()
	print("depth", response.reason, response.status)

	resp = json.load(response)
	return resp['btc_usd']

def get_ticker():
	# convert parms to url format
	parms = {
		"method": "ticker",
		"pair": "btc_usd",
	}
	parms = urllib.urlencode(parms)
	# may add .parse()
	# hash api secret
	hashed = hmac.new(API_SECRET, digestmod=hashlib.sha512)
	# update parms
	hashed.update(parms)
	# create signature
	signature = hashed.hexdigest()

	# create the headers and key and sign elements to it
	headers = {"Content-type": "application/x-www-form-urlencoded",
			   "Key": API_KEY,
			   "Sign": signature}

	# establish a connection
	conn = httplib.HTTPSConnection("btc-e.com")
	conn.request("GET", "/api/3/ticker/btc_usd", parms, headers)

	response = conn.getresponse()
	print("ticker", response.reason, response.status)

	resp = json.load(response)
	return resp

def get_last_price():
	return get_ticker()['btc_usd']['last']

def get_weight_diff():
	ba = get_depth()
	b = ba['bids']
	a = ba['asks']
	bid_weight = 0
	ask_weight = 0

	for each in b:
		bid_weight += each[0] * each[1]

	for each in a:
		ask_weight += each[0]*each[1]

	return bid_weight-ask_weight

time_length = 3
count = 0
diffs = []
prices = []
times = [i for i in range(0, time_length*2, 2)]
while count < time_length:
	diffs.append(get_weight_diff())
	prices.append(get_last_price())
	count += 1
	print(count)
	time.sleep(2)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(times, diffs, color="red")

ax2 = ax1.twinx()
plt.scatter(times, prices, color="blue")
# TODO fix matplotlib bullshit
fig.show()
