# Monte Carlo Option Pricing

Multi-step Monte Carlo engine in Python to simulate equity price dynamics under a risk-neutral Geometric Brownian Motion framework and price both standard and path-dependent derivatives.

## Project Structure

```
monte-carlo-option-pricing/
│
├── monte_carlo.py      # Main simulation engine and pricing logic
├── black_scholes.py    # Analytical Black-Scholes formulas
├── plots.py            # Visualisation utilities
├── README.md
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python monte_carlo.py
```

---

## Model

### Stock Price Dynamics

Stock price follows Geometric Brownian Motion (GBM):

```math
dS_t = rS_t \, dt + \sigma S_t \, dW_t
```

### Discretisation

```math
S_{t+1} = S_t \exp\!\left(\left(r - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t}\, Z\right)
```

where $Z \sim \mathcal{N}(0,1)$.

### Option Pricing

Option price estimated via discounted expectation:

```math
C = e^{-rT} \, \mathbb{E}\!\left[\max(S_T - K,\, 0)\right]
```

### Variance Reduction

Antithetic variates are used to reduce estimator variance:

```math
Z \;\longrightarrow\; (Z,\,-Z)
```

---

## Options Priced

| Option | Type | Description |
|---|---|---|
| European Call | Vanilla | Payoff: $\max(S_T - K, 0)$ |
| European Put | Vanilla | Payoff: $\max(K - S_T, 0)$ |
| Asian Call | Path-dependent | Payoff based on arithmetic average price |
| Barrier Call | Path-dependent | Up-and-out: knocked out if $S_t \geq B$ |

---

## Parameters

| Parameter | Symbol | Default |
|---|---|---|
| Initial stock price | $S_0$ | 100 |
| Strike price | $K$ | 110 |
| Time to expiry | $T$ | 1.0 year |
| Risk-free rate | $r$ | 0.05 |
| Volatility | $\sigma$ | 0.20 |
| Barrier level | $B$ | 140 |
| Simulations | $N$ | 10,000 |
| Time steps | — | 252 |

---

## Validation

Monte Carlo prices are benchmarked against closed-form Black–Scholes values. At the default parameters the MC call price converges to the analytical value of ~6.04, confirming the simulation is correctly implemented.
