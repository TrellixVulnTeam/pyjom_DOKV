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
threshold = 30
# print(xLeftPointsFiltered.shape)
# breakpoint()
xLeftPointsSignal = (abs(xLeftPointsFiltered - xLeftPoints) < threshold).astype(np.uint8) # convert this shit to intervals! # (589, 589), how the fuck?
# print(xLeftPointsSignal.shape)
# breakpoint()
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

xLeftPointsSignalList = xLeftPointsSignal.tolist()
print(xLeftPointsSignal.shape)
# print(xLeftPointsSignalList)
spanLengthMinThreshold = 10
kalmanMaxSlope = 0.10
xLeftSpans = extract_span(xLeftPointsSignalList, target=1)

from sklearn.linear_model import LinearRegression


stablePipRangeTuples = [] # remember this is only xLeftSpans, not for all!

for start, end in xLeftSpans:
    spanLength = end-start

    print(start, end, coef)
    if spanLength > spanLengthMinThreshold:
        kalmanSegment = xLeftPointsFiltered[start:end+1].reshape(-1,1)
        model = LinearRegression()
        X,y = kalmanSegment,np.linspace(0, end-start,end-start+1)
        model.fit(X,y)
        coef = model.coef_[0]
        if abs(coef) < kalmanMaxSlope:
            kalmanMean = np.mean(kalmanSegment)
            stablePipRangeTuples.append({"frameSpan": (start, end), 'mean': kalmanMean})
            xLeftPointsSignal[start:end] = kalmanMean

# exit()
# print(xLeftPoints)
for stablePipRangeTuple in stablePipRangeTuples:
    print(stablePipRangeTuple)
exit()
import matplotlib.pyplot as plt

plt.plot(xLeftPoints)
plt.plot(xLeftPointsFiltered)
plt.plot(xLeftPointsSignal)
plt.show()

