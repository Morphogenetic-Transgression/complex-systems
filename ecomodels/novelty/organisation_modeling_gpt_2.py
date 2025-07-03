import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Parameters
k = 1.0  # Boltzmann constant
T = 1.0  # Temperature
E_high = 5.0
E_low = 0  # -5.0
n_energy_steps = 80
n_flips_per_energy = 5

# Energy values over time
E_B_values_one_cycle = np.repeat(
    np.linspace(E_high, E_low, n_energy_steps), n_flips_per_energy
)
E_B_values = np.concatenate(
    [E_B_values_one_cycle, E_B_values_one_cycle]
)  # Two full cycles
total_frames = len(E_B_values)


P_A = lambda E_B: np.exp(-0 / (k * T)) / (np.exp(-0 / (k * T)) + np.exp(-E_B / (k * T)))
P_B = lambda E_B: 1 - P_A(E_B)

# Setup figure and axes
fig, axs = plt.subplots(1, 4, figsize=(20, 5))
fig.suptitle("Bit Relaxation and Flipping Behavior Over Energy Gradient \n")

bars = []
particle = None
bit_texts = []
energy_bar = None


def init():
    for ax in axs:
        ax.clear()

    # --- Boxes and Particle ---
    axs[0].set_title("Boxes (Bit States)")
    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(0, 1)
    axs[0].axis("off")
    axs[0].add_patch(
        plt.Rectangle((0.2, 0.4), 0.2, 0.2, fill=None, edgecolor="blue", lw=2)
    )  # Box A
    axs[0].add_patch(
        plt.Rectangle((0.6, 0.4), 0.2, 0.2, fill=None, edgecolor="red", lw=2)
    )  # Box B
    global particle
    particle = axs[0].add_patch(plt.Circle((0.3, 0.5), 0.03, color="blue"))

    # Bit text labels
    bit_texts.clear()
    bit_texts.append(
        axs[0].text(0.27, 0.15, "1", ha="center", fontsize=16, color="blue")
    )
    bit_texts.append(
        axs[0].text(0.73, 0.15, "0", ha="center", fontsize=16, color="red")
    )

    # --- Probability Distribution ---
    axs[1].set_title("Probability Distribution")
    bars.clear()
    bars.append(axs[1].bar(["A", "B"], [1, 0], color=["blue", "red"]))
    axs[1].set_ylim(0, 1)

    # --- Entropy Plot ---
    axs[2].set_title("Entropy")
    bars.append(axs[2].bar(["Entropy"], [0], color="gray"))
    axs[2].set_ylim(0, 1)

    # --- Energy Bar ---
    axs[3].set_title("Energy of Box B")
    global energy_bar
    energy_bar = axs[3].bar(["E_B"], [E_high], color="purple")
    axs[3].set_ylim(E_low - 1, E_high + 1)

    return bars + [particle] + bit_texts + [energy_bar]


def update(frame):
    E_B = E_B_values[frame]
    p_a = P_A(E_B)
    p_b = P_B(E_B)
    S = -p_a * np.log2(p_a) - p_b * np.log2(p_b) if p_a > 0 and p_b > 0 else 0

    # Update probability bars
    for bar, val in zip(bars[0], [p_a, p_b]):
        bar.set_height(val)
    bars[1][0].set_height(S)

    # Update energy bar
    energy_bar[0].set_height(E_B)

    # Randomly place particle
    if np.random.rand() < p_a:
        particle.set_center((0.3, 0.5))
        particle.set_color("blue")
        bit_texts[0].set_text("1")
        bit_texts[1].set_text("0")
    else:
        particle.set_center((0.7, 0.5))
        particle.set_color("red")
        bit_texts[0].set_text("0")
        bit_texts[1].set_text("1")

    return bars + [particle] + bit_texts + [energy_bar]


ani = animation.FuncAnimation(
    fig, update, frames=total_frames, init_func=init, blit=False, interval=20
)

from matplotlib.animation import FFMpegWriter

writer = FFMpegWriter(
    fps=10, metadata=dict(artist="Bit Engine Simulation"), bitrate=1800
)
ani.save("bit_relaxation_two_cycles.mp4", writer=writer)

# plt.show()
