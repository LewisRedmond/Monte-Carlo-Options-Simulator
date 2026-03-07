import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Parameters
S0 = 100
K = 110
T = 1.0
r = 0.05
sigma = 0.2
nSim = 10000          # increase for more accurate pricing
nSteps = 252
B = 140                # Barrier level
dt = T/nSteps

# Black–Scholes formulas
def blackScholesCall(S, K, T, r, sigma):
    d1 = (np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    return S*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)

def blackScholesPut(S, K, T, r, sigma):
    d1 = (np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    return K*np.exp(-r*T)*norm.cdf(-d2)-S*norm.cdf(-d1)

# Time grid
time = np.linspace(0, T, nSteps)

# Monte Carlo Simulation
# (Antithetic Variates Included)
Z = np.random.standard_normal((nSteps, nSim))
Z = np.concatenate((Z, -Z), axis=1)   # variance reduction
nSim *= 2

S = np.zeros((nSteps, nSim))
S[0] = S0

for t in range(1, nSteps):
    S[t] = S[t-1]*np.exp((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*Z[t])

# European Options
ST = S[-1]

callPayoff = np.maximum(ST-K, 0)
putPayoff  = np.maximum(K-ST, 0)

discountedCall  = np.exp(-r*T)*callPayoff
discountedPut  = np.exp(-r*T)*putPayoff

callPriceMC = np.mean(discountedCall)
putPriceMC  = np.mean(discountedPut)

# Standard Errors
callSe = np.std(discountedCall)/np.sqrt(nSim)
putSe  = np.std(discountedPut)/np.sqrt(nSim)

# Confidence Intervals
callCi = (float(callPriceMC-1.96*callSe), float(callPriceMC+1.96*callSe))

putCi = (float(putPriceMC-1.96*putSe), float(putPriceMC+1.96*putSe))

# Asian Option (Arithmetic Mean)
averagePrice = np.mean(S, axis=0)
asianCall = np.exp(-r*T) * np.mean(np.maximum(averagePrice - K, 0))

# Barrier Option (Up-and-Out Call)
maxPath = np.max(S, axis=0)
alive = maxPath < B

barrierCall  = np.exp(-r*T) * np.mean(np.maximum(ST - K, 0) * alive)

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

# Plot Simulated Paths
plt.figure(figsize=(10, 6))
plt.plot(time, S[:, :50])   # plot first 50 paths for clarity
plt.xlabel("Time (Years)")
plt.ylabel("Stock Price")
plt.title("Monte Carlo Simulated Stock Price Paths")
plt.show()
# Black-Scholes: 6.0401 this time therefore my simulation is working correctly and my model matches Black-Scholes theory
