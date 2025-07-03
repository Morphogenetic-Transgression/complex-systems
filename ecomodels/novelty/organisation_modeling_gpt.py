import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Simulation Parameters
k = 1.0  # Boltzmann constant (arbitrary units)
T = 1.0  # Temperature
E_high = 5.0  # Energy of state B (Box B)
E_low = 0.0  # Energy of state A (Box A)

# Simulation over relaxation steps
n_energy_steps = 100
n_flips_per_energy = 5
total_frames = n_energy_steps * n_flips_per_energy
E_B_values = np.repeat(np.linspace(E_high, E_low, n_energy_steps), n_flips_per_energy)

"""
E_B_values = np.concatenate(
    [
        np.linspace(E_high, E_low, n_frames // 2),
        np.linspace(E_low, -E_high, n_frames // 2),
    ]
)
"""

P_A = lambda E_B: np.exp(-E_low / (k * T)) / (
    np.exp(-E_low / (k * T)) + np.exp(-E_B / (k * T))
)
P_B = lambda E_B: 1 - P_A(E_B)

# Prepare animation figure
fig, axs = plt.subplots(1, 3, figsize=(12, 4))
fig.suptitle("Relaxation from Sharp Energy Gradient to Thermal Equilibrium \n")

box_A_pos = [0.3, 0.5]
box_B_pos = [0.7, 0.5]

bars = []

import matplotlib.patches as patches

# Add global particle artist
particle = None


def init_with_particle():
    for ax in axs:
        ax.clear()
    axs[0].set_title("Boxes (Bit States)")
    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(0, 1)
    axs[0].axis("off")

    # Draw boxes
    axs[0].add_patch(
        plt.Rectangle((0.2, 0.4), 0.2, 0.2, fill=None, edgecolor="blue", lw=2)
    )  # Box A
    axs[0].add_patch(
        plt.Rectangle((0.6, 0.4), 0.2, 0.2, fill=None, edgecolor="red", lw=2)
    )  # Box B

    # Add particle in initial state (Box A)
    global particle
    particle = axs[0].add_patch(plt.Circle((0.3, 0.5), 0.03, color="blue"))

    bars.clear()
    bars.append(axs[1].bar(["A", "B"], [1, 0], color=["blue", "red"]))
    axs[1].set_ylim(0, 1)
    axs[1].set_title("Probability Distribution")
    bars.append(axs[2].bar(["Entropy"], [0], color="gray"))
    axs[2].set_ylim(0, 1)
    axs[2].set_title("Entropy")
    return bars + [particle]


def update_with_particle(frame):
    E_B = E_B_values[frame]
    p_a = P_A(E_B)
    p_b = P_B(E_B)

    # Shannon entropy
    S = -p_a * np.log2(p_a) - p_b * np.log2(p_b) if p_a > 0 and p_b > 0 else 0

    # Update bars
    for bar, val in zip(bars[0], [p_a, p_b]):
        bar.set_height(val)
    bars[1][0].set_height(S)

    # Update particle position based on probability
    if np.random.rand() < p_a:
        particle.set_center((0.3, 0.5))  # Box A
        particle.set_color("blue")
    else:
        particle.set_center((0.7, 0.5))  # Box B
        particle.set_color("red")

    return bars + [particle]


ani_with_particle = animation.FuncAnimation(
    fig,
    update_with_particle,
    frames=total_frames,
    init_func=init_with_particle,
    blit=False,
    interval=150,
)

plt.show()

"""
plt.tight_layout()
plt.close(fig)
ani
"""
