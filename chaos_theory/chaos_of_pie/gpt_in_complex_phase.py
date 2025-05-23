import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Torus parameters
R = 2  # Major radius
r = 1  # Minor radius

# Phase sampling
theta = np.linspace(0, 100 * np.pi, 4000)

# Angular components: arguments of complex numbers
phi = np.mod(theta, 2 * np.pi)  # arg(e^{iθ})
psi = np.mod(np.pi * theta, 2 * np.pi)  # arg(e^{iπθ})

# 3D embedding of Arg(θ), Arg(πθ) into torus
x = (R + r * np.cos(psi)) * np.cos(phi)
y = (R + r * np.cos(psi)) * np.sin(phi)
z = r * np.sin(psi)

# Setup 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
(line,) = ax.plot([], [], [], lw=1.5, color="blue")
(point,) = ax.plot([], [], [], "ro")

# Torus surface (optional)
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, 2 * np.pi, 30)
U, V = np.meshgrid(u, v)
X = (R + r * np.cos(V)) * np.cos(U)
Y = (R + r * np.cos(V)) * np.sin(U)
Z = r * np.sin(V)
ax.plot_surface(X, Y, Z, alpha=0.1, color="gray")

# Axis settings
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([-1.5, 1.5])
ax.set_box_aspect([1, 1, 0.6])


# Init and update functions
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point


def update(frame):
    n = frame * 5
    line.set_data(x[:n], y[:n])
    line.set_3d_properties(z[:n])
    point.set_data(x[n - 1 : n], y[n - 1 : n])
    point.set_3d_properties(z[n - 1 : n])
    ax.view_init(elev=30, azim=frame * 0.7)
    return line, point


# Animate
frames = len(theta) // 5
ani = FuncAnimation(fig, update, init_func=init, frames=frames, blit=True, interval=30)

plt.show()
