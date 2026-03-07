import matplotlib.pyplot as plt

# Plot Simulated Paths
plt.figure(figsize=(10, 6))
plt.plot(time, S[:, :50])   # plots the first 50 paths for clarity
plt.xlabel("Time (Years)")
plt.ylabel("Stock Price")
plt.title("Monte Carlo Simulated Stock Price Paths")
plt.show()
