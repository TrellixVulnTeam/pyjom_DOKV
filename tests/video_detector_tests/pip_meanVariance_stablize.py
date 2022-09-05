import json

data = json.loads(open("pip_meanVariance.json",'r').read())


# print(len(data)) # 589
import numpy as np
data = np.array(data)
from pykalman import KalmanFilter

def Kalman1D(observations,damping=0.2):
    # To return the smoothed time series data
    observation_covariance = damping
    initial_value_guess = observations[0]
    transition_matrix = 1
    transition_covariance = 0.1
    initial_value_guess
    kf = KalmanFilter(
            initial_state_mean=initial_value_guess,
            initial_state_covariance=observation_covariance,
            observation_covariance=observation_covariance,
            transition_covariance=transition_covariance,
            transition_matrices=transition_matrix
        )
    pred_state, state_cov = kf.smooth(observations)
    return pred_state

xLeftPoints = data[:,0,1]
xLeftPointsFiltered = Kalman1D(xLeftPoints)
xLeftPointsFiltered=xLeftPointsFiltered.reshape(-1)
from itertools import groupby
def extract_span(mlist, target=0):
    counter = 0
    spanList = []
    target_list = [(a,len(list(b))) for a,b in groupby(mlist)]
    for a,b in target_list:
        nextCounter = counter+b
        if a == target:
            spanList.append((counter, nextCounter))
        counter = nextCounter
    return spanList

# solve diff.
xLeftPointsFilteredDiff = np.diff(xLeftPointsFiltered)
# xLeftPointsFilteredDiff3 = np.diff(xLeftPointsFilteredDiff)

# xLeftPointsFilteredDiff3Filtered = Kalman1D(xLeftPointsFilteredDiff3)
derivativeThreshold = 3
# derivative3Threshold = 3
xLeftPointsSignal = (abs(xLeftPointsFilteredDiff) < derivativeThreshold).astype(np.uint8).tolist()

def signalFilter(signal, threshold = 10):
    newSignal = np.zeros(len(signal))
    signalFiltered = extract_span(xLeftPointsSignal, target=1)
    newSignalRanges = []
    for start, end in signalFiltered:
        length = end-start
        if length >= threshold:
            newSignalRanges.append((start, end))
            newSignal[start:end+1] = 1
    return newSignal, newSignalRanges

xLeftPointsSignalFiltered, newSignalRanges= signalFilter(xLeftPointsSignal)
xLeftPointsSignalFiltered *=255

mShrink = 4
for start, end in newSignalRanges:
    # could we shrink the boundaries?
    std = np.std(xLeftPointsFiltered[start+mShrink:end+1])
    print((start, end), std)

import matplotlib.pyplot as plt

# plt.plot(xLeftPoints)
# plt.plot(xLeftPointsFiltered)
# plt.plot(xLeftPointsFilteredDiff)
# # plt.plot(xLeftPointsFilteredDiff3)
# plt.plot(xLeftPointsSignalFiltered)
# plt.show()

