import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def kalman(data, initial_estimate, initial_estimate_error, data_error):
    estimate_error = float(initial_estimate_error)
    estimate = float(initial_estimate)
    # length of estimates array should be one more than length of data because it includes your original guess
    estimates = [estimate]
    print(estimate)
    for each in data:
        # Part 1: Calculate kalman gain
        kg = estimate_error/(estimate_error+data_error)

        # Part 2: Append and calculate current estimate
        prev_estimate = estimate
        estimate = prev_estimate + kg*(each - prev_estimate)
        estimates.append(estimate)

        # Part 3: Calculate new error in estimate
        estimate_error = (1-kg)*estimate_error


    print("The next estimate should be " +str(estimates[-1]) + " with an error of about " +str(estimate_error)
      + " assuming data_error is reasonable and there are enough iterations.")
    return estimates

inf = open('/home/keyan/fun/algotrading/DAT_MT_EURUSD_M1_201607.csv')
prices = []
time = []
count = 0

estimate=0
error=2

for line in inf:
    if count<20:
        raw = line.split(',')
        for i in range(2,6):
            prices += [float(raw[i])]
            count += 1
            time.append(count)
    else:
        break

# Kalman estimates
intial_estimate = 1.1
initial_estimate_error = .1
data_error = .1

estimates = kalman(prices, initial_estimate, initial_estimate_error, data_error)

plt.subplots()
plt.plot(time, prices, 'ro')
plt.plot(time, estimates[1:], 'bo')
plt.show()
