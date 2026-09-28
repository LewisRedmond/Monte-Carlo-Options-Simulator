import numpy as np
from scipy.stats import norm
from black_scholes import blackScholesCall, blackScholesPut

np.random.seed(42)# Makes the random number generator start at 42 each time

# Parameters
S0 = 100
K = 110
T = 1.0
r = 0.05
sigma = 0.2
nSim = 10000 # Increase for more accurate price
nSteps = 252
B = 140 # Barrier level
dt = T/nSteps
# Time grid
time = np.linspace(0, T, nSteps+1)
# Monte Carlo Simulation
def pathSimulator(S0, r, sigma, T, nSteps, nSim, dt):
    Z = np.random.standard_normal((nSteps, nSim))
    Z = np.concatenate((Z, -Z), axis=1)   # variance reduction
    nSim *= 2
    S = np.zeros((nSteps+1, nSim))
    S[0] = S0
    for t in range(1, nSteps+1):
        S[t] = S[t-1]*np.exp((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*Z[t-1])
    return S

S = pathSimulator(S0, r, sigma, T, nSteps, nSim, dt)

# European Options
ST = S[-1]
callPayoff = np.maximum(ST-K, 0)
putPayoff  = np.maximum(K-ST, 0)
discountedCall  = np.exp(-r*T)*callPayoff
discountedPut  = np.exp(-r*T)*putPayoff
callPriceMC = np.mean(discountedCall)
putPriceMC  = np.mean(discountedPut)

# Standard Errors
callSe = np.std(discountedCall)/np.sqrt(len(discountedCall))
putSe  = np.std(discountedPut)/np.sqrt(len(discountedPut))

# Confidence Intervals
callCi = (float(callPriceMC-1.96*callSe), float(callPriceMC+1.96*callSe))
putCi = (float(putPriceMC-1.96*putSe), float(putPriceMC+1.96*putSe))

# Asian Option (Arithmetic Mean)
averagePrice = np.mean(S, axis=0)
asianCall = np.exp(-r*T)*np.mean(np.maximum(averagePrice-K, 0))

# Barrier Option (Up-and-Out Call)
maxPath = np.max(S, axis=0)
alive = maxPath < B
barrierCall  = np.exp(-r*T)*np.mean(np.maximum(ST-K, 0) * alive)

# Black–Scholes Comparison
bsCall = blackScholesCall(S0, K, T, r, sigma)
bsPut  = blackScholesPut(S0, K, T, r, sigma)

# Output Results
print("====== European Call ======")
print("Monte Carlo Price:", callPriceMC)
print("Std Error:", callSe)
print("95% CI:", callCi)
print("Black–Scholes:", bsCall)

print("\n====== European Put ======")
print("Monte Carlo Price:", putPriceMC)
print("Std Error:", putSe)
print("95% CI:", putCi)
print("Black–Scholes:", bsPut)

print("\n====== Asian Options ======")
print("Asian Call:", asianCall)
print("Barrier Call (Up-and-Out):", barrierCall )

from plots import plotPaths
plotPaths(time, S)
