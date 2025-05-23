import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parameters
R = 2  # Major radius
r = 1  # Minor radius
theta = np.linspace(0, 20 * np.pi, 3000)  # Path sampling

# Parametrize trajectory on torus
phi = theta
psi = np.pi * theta

x = (R + r * np.cos(psi)) * np.cos(phi)
y = (R + r * np.cos(psi)) * np.sin(phi)
z = r * np.sin(psi)

# Create figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
(line,) = ax.plot([], [], [], lw=2, color="blue")
(point,) = ax.plot([], [], [], "ro")

# Torus surface (optional context)
u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, 2 * np.pi, 30)
U, V = np.meshgrid(u, v)
X = (R + r * np.cos(V)) * np.cos(U)
Y = (R + r * np.cos(V)) * np.sin(U)
Z = r * np.sin(V)
ax.plot_surface(X, Y, Z, alpha=0.1, color="gray")

# Set limits and appearance
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-1.5, 1.5])
ax.set_box_aspect([1, 1, 0.6])  # keep torus round


# Initialization function
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point


# Update function with rotating view
def update(frame):
    n = frame * 5
    line.set_data(x[:n], y[:n])
    line.set_3d_properties(z[:n])
    point.set_data(x[n - 1 : n], y[n - 1 : n])
    point.set_3d_properties(z[n - 1 : n])

    # Rotate camera view
    ax.view_init(elev=30, azim=frame * 0.7)
    return line, point


# Run animation
frames = len(theta) // 5
ani = FuncAnimation(fig, update, init_func=init, frames=frames, blit=True, interval=30)

plt.show()
