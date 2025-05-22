import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 100, 10000)
x = np.mod(theta, 2 * np.pi)
y = np.mod(np.pi * theta, 2 * np.pi)

plt.plot(x, y, ".", markersize=0.5)
plt.xlabel("θ mod 2π")
plt.ylabel("πθ mod 2π")
plt.title("Trajectory on the 2-Torus")
plt.show()
