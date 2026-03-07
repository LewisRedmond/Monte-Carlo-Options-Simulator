# Monte-Carlo-Options-Simulator
Multi-step Monte Carlo engine in Python to simulate equity price dynamics under a risk neutral Geometric Brownian Motion framework and price both standard and path dependent derivatives.

# Model
Stock price follows Geometric Brownian Motion:
```math
dS_t = rS_t dt + σS_t dW_t
```
Discretisation:
```math
S_t+1 = S_t exp((r - \frac{1}{2} σ^2)Δt + σ \sqrt{Δt} Z
```
Pricing
Option price estimated via:
``` math
C = e^{-rT}E[max(S_T - K, 0)]
```
Variance Reduction
Antithetic variates used:
``` math
Z -> (Z, -Z)
```
