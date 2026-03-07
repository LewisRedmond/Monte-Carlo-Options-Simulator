import matplotlib.pyplot as plt

# Plot Simulated Paths
def plotPaths(time, S, n=50):
  plt.figure(figsize=(10, 6))
  plt.plot(time, S[:, :n])   # plots the first 50 paths for clarity
  plt.xlabel("Time (Years)")
  plt.ylabel("Stock Price")
  plt.title("Monte Carlo Simulated Stock Price Paths")
  plt.show()
