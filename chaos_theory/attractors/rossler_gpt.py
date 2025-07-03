from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import numpy as np
from matplotlib import pyplot as plt

# Parameters for animation
c_values_anim = np.linspace(3.5, 6.0, 50)
n_steps = 3000
dt = 0.01

# Store trajectories for entropy and Fourier
time_series_by_c = []

# Prepare figure
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")
(line,) = ax.plot([], [], [], lw=0.5)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(0, 30)
ax.set_title("Rössler System: Transition to Chaos")

# Normalize colors to visualize parameter c
norm = Normalize(vmin=min(c_values_anim), vmax=max(c_values_anim))
cmap = plt.cm.plasma
sm = ScalarMappable(cmap=cmap, norm=norm)

# Initial state
state = np.array([1.0, 1.0, 1.0])


def rossler_step(state, a=0.2, b=0.2, c=5.7):
    x, y, z = state
    dx = -y - z
    dy = x + a * y
    dz = b + z * (x - c)
    return np.array([x + dx * dt, y + dy * dt, z + dz * dt])


def init():
    line.set_data([], [])
    line.set_3d_properties([])
    return (line,)


def update(frame):
    global state
    c = c_values_anim[frame]
    state = np.array([1.0, 1.0, 1.0])
    traj = np.zeros((n_steps, 3))
    for i in range(n_steps):
        state = rossler_step(state, c=c)
        traj[i] = state
    time_series_by_c.append(traj[:, 0])  # store x(t) for entropy/Fourier
    color = cmap(norm(c))
    line.set_data(traj[:, 0], traj[:, 1])
    line.set_3d_properties(traj[:, 2])
    line.set_color(color)
    ax.set_title(f"Rössler Attractor (c = {c:.2f})")
    return (line,)


# Animate
ani = FuncAnimation(
    fig, update, frames=len(c_values_anim), init_func=init, blit=False, repeat=False
)

"""
plt.close(fig)  # Avoid displaying static frame here
ani.save("/mnt/data/rossler_transition_to_chaos.mp4", writer="ffmpeg", fps=10)
"""

"/mnt/data/rossler_transition_to_chaos.mp4"
