"""
plan:
    поиск хаоса в трансцендентальности
    draw pi curve (double pendelum trajectory) z(theta) = exp(theta * i) + exp(pi * theta * i)
    draw ints phase trajectory. to show that velocity never repits itself so that no point on phase plane repits
    show that that is a determitate chaos.
    chaos is in pi's transcendentality. chaotic series of digits. I can visualise this series in a different ways
    describe the connection

    траектория никогда не зацикливается

    inspired by Lourenze Attractor and this visualisation of irrational nature of pi

    I thought there is Deterministic Chaos in pi but there is not

    Phase Space = (exp(theta * i), exp(pi * theta * i));
    Phase Projection (Torus) = (theta mod 2pi, pi * theta mod 2pi);
    Embedding of Phase Projection in R^3. Pase Trajectory does not intersect itself.

    I have seen this animation. The curve never closes. So I thought that there might be some othere curve in some other
    space that does not intersect itself. This curve actualy lives in C^2 (formula). But in order to visualise it I had to draw an
    embedding in R^3 of phase projection which is torus.

"""

from typing import List
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider


class QuasiPeriodicPiSystem:

    def __init__(
        self,
        step_init=0,
        steps_number=4000,
        frequencies=[1, np.pi],
        torus_R=4,
        torus_r=2,
    ):
        self.step = step_init
        self.theta = np.linspace(0, 200 * np.pi, steps_number)
        self.frequencies = frequencies
        self.torus_R = torus_R
        self.torus_r = torus_r
        self._calculate_parameters()

    def _inC2(self) -> np.ndarray:
        return sum(
            [np.exp(1j * frequency * self.theta) for frequency in self.frequencies]
        )

    def _calculate_parameters(self) -> None:
        self.cycles_number = (self.theta / (2 * np.pi)).astype(int)

        inC2 = self._inC2()  # z.real z.imag
        self.plane_x = 2 * inC2.real
        self.plane_y = 2 * inC2.imag

        if len(self.frequencies) == 2:
            u = self.theta * self.frequencies[0]
            v = self.theta * self.frequencies[1]

            self.torus_x = self.torus_R * np.cos(u) + self.torus_r * np.cos(v) * np.cos(
                u
            )
            self.torus_y = self.torus_R * np.sin(u) + self.torus_r * np.cos(v) * np.sin(
                u
            )
            self.torus_z = self.torus_r * np.sin(v)
        else:
            print("No torus")


# constants

STEPS_IN_SIMULATION = 10000
SIMULATION_ANIMATION_RATIO = 1
FRAMES_NUMBER = STEPS_IN_SIMULATION // SIMULATION_ANIMATION_RATIO
DELAY_BETWEEN_FRAMES_MILLISEC = 20

SURFACE_WIDTH = 10
SURFACE_HEIGHT = 10

SIMULATION_NAME = r"Transcendentality of $\pi$ causes Quasiperiodicity"


# utilites
def axis_initialize(ax, index_, title, title_color=None):

    ax.set_title(title)
    if title_color:
        ax.set_title(title, color=title_color)
    ax.set_aspect("equal")
    ax.set_xlim(-SURFACE_WIDTH / 2, SURFACE_WIDTH / 2)
    ax.set_ylim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
    ax.set(xlabel=r"Re", ylabel=r"Im")
    ax.set_xticks([]),
    ax.set_yticks([])

    """
    scatter_size = 10
    scatter = ax.scatter([], [], scatter_size)
    scatter.set_color("red")
    """

    (scatter,) = ax.plot([], [], "ro")
    (trail,) = ax.plot([], [], "b-", lw=0.3)

    text = None
    if index_ == 1:
        text = ax.text(-(SURFACE_HEIGHT / 2) * 0.92, (SURFACE_HEIGHT / 2) * 0.92, s="")

    return scatter, trail, text


def axis_draw_dynamics(scatter, trail, text, system, step):

    if text:
        text.set_text(f"cycles number: {system.cycles_number[step-1]}")

    scatter.set_data(system.plane_x[step - 1 : step], system.plane_y[step - 1 : step])

    trail.set_data(system.plane_x[:step], system.plane_y[:step])

    return scatter, trail, text


def axis_3d_initialize(ax, index_, title):

    ax.set_title(title)
    # ax.set_aspect("equal")
    ax.set_xlim(-SURFACE_WIDTH / 2, SURFACE_WIDTH / 2)
    ax.set_ylim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
    ax.set_zlim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
    ax.set(
        xlabel=r"$\cos(\theta) \cdot (1 + \cos(\pi \cdot \theta))$",
        ylabel=r"$\sin(\theta) \cdot (1 + \cos(\pi \cdot \theta))$",
        zlabel=r"$\sin(\pi \cdot \theta)$",
    )
    ax.set_xticks([]),
    ax.set_yticks([])
    ax.set_zticks([])

    (scatter,) = ax.plot([], [], [], "ro")
    (trail,) = ax.plot([], [], [], "b-", lw=0.5)

    return scatter, trail


def axis_3d_draw_dynamics(scatter, trail, system, step):

    scatter.set_data(system.torus_x[step - 1 : step], system.torus_y[step - 1 : step])
    scatter.set_3d_properties(system.torus_z[step - 1 : step])

    trail.set_data(system.torus_x[:step], system.torus_y[:step])
    trail.set_3d_properties(system.torus_z[:step])

    return scatter, trail


# system init
system_1 = QuasiPeriodicPiSystem(
    step_init=0,
    steps_number=STEPS_IN_SIMULATION,
    frequencies=[1],
    torus_R=4,
    torus_r=2,
)
system_2 = QuasiPeriodicPiSystem(
    step_init=0,
    steps_number=STEPS_IN_SIMULATION,
    frequencies=[1, 3],
    torus_R=4,
    torus_r=2,
)
system_3 = QuasiPeriodicPiSystem(
    step_init=0,
    steps_number=STEPS_IN_SIMULATION,
    frequencies=[1, np.pi],
    torus_R=4,
    torus_r=2,
)

# plotting attributes
fig = plt.figure(figsize=(20, 10))
fig.suptitle(SIMULATION_NAME, fontsize=14)
gs = gridspec.GridSpec(2, 3)

ax1 = fig.add_subplot(gs[0, 0])
box1 = ax1.get_position()
ax1.set_position([box1.x0 - 0.1, box1.y0 - 0.0, box1.width * 1, box1.height * 1])

ax2 = fig.add_subplot(gs[1, 0])
box2 = ax2.get_position()
ax2.set_position([box2.x0 - 0.1, box2.y0 - 0.0, box2.width * 1, box2.height * 1])

ax3 = fig.add_subplot(gs[:, 1])
box3 = ax3.get_position()
ax3.set_position([box3.x0 - 0.12, box3.y0 - 0.07, box3.width * 1.2, box3.height * 1.2])

ax4 = fig.add_subplot(gs[:, 2], projection="3d")
box4 = ax4.get_position()
ax4.set_position([box4.x0 - 0.11, box4.y0 - 0.17, box4.width * 1.8, box4.height * 1.8])


scatter_1, trail_1, text_1 = axis_initialize(
    ax1, 1, title=r"$z = e^{i \cdot \theta}$" + " (periodic)"
)
scatter_2, trail_2, text_2 = axis_initialize(
    ax2,
    2,
    title=r"$z = e^{i \cdot \theta} + e^{3 \cdot i \cdot \theta}$" + " (periodic)",
)
scatter_3, trail_3, text_3 = axis_initialize(
    ax3,
    3,
    title=r"$z = e^{i \cdot \theta} + e^{\pi \cdot i \cdot \theta}$"
    + " (quasi-periodic because of "
    + r"$\pi$)"
    + "\n The curve never closes.",
    title_color="r",
)

scatter_3d, trail_3d = axis_3d_initialize(
    ax4,
    4,
    title="Phase Projection of "
    + r"$(e^{i \cdot \theta}, e^{\pi \cdot i \cdot \theta})$"
    + " embedded into "
    + r"$\mathbb{R}^3$"
    + ". Phase Trajectory does not intersect itself.",
)

# Torus surface (optional)
"""
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, 2 * np.pi, 30)
U, V = np.meshgrid(u, v)
X = (system_3.torus_R + system_3.torus_r * np.cos(V)) * np.cos(U)
Y = (system_3.torus_R + system_3.torus_r * np.cos(V)) * np.sin(U)
Z = system_3.torus_r * np.sin(V)
ax4.plot_surface(X, Y, Z, alpha=0.1, color="gray")
"""

# animation

paused = [True]
step = 1


def update_plot(frame):

    global SIMULATION_ANIMATION_RATIO, step, text_1, scatter_1, trail_1, text_2, scatter_2, trail_2, text_3, scatter_3, trail_3, scatter_3d, trail_3d

    if (not paused[0]) and step < STEPS_IN_SIMULATION:

        scatter_1, trail_1, text_1 = axis_draw_dynamics(
            scatter_1, trail_1, text_1, system_1, step
        )

        scatter_2, trail_2, text_2 = axis_draw_dynamics(
            scatter_2, trail_2, text_2, system_2, step
        )

        scatter_3, trail_3, text_3 = axis_draw_dynamics(
            scatter_3, trail_3, text_3, system_3, step
        )

        scatter_3d, trail_3d = axis_3d_draw_dynamics(
            scatter_3d, trail_3d, system_3, step
        )

        step += SIMULATION_ANIMATION_RATIO

    return (
        text_1,
        scatter_1,
        trail_1,
        scatter_2,
        trail_2,
        scatter_3,
        trail_3,
        scatter_3d,
        trail_3d,
    )


animation = FuncAnimation(
    fig=fig,
    func=update_plot,
    frames=FRAMES_NUMBER,
    interval=DELAY_BETWEEN_FRAMES_MILLISEC,
    blit=True,
)


# wigets

# button
button_ax = plt.axes([0.8, 0.025, 0.1, 0.04])  # x, y, width, height
button = Button(button_ax, "Play", hovercolor="0.975")


def toggle(event):
    paused[0] = not paused[0]
    button.label.set_text("Play" if paused[0] else "Pause")


button.on_clicked(toggle)


# Slider
slider_ax = plt.axes([0.3, 0.1, 0.2, 0.03])  # [left, bottom, width, height]
# slider_min = 10
# slider_max = 200
slider_min = 1
slider_max = 10
slider_init = SIMULATION_ANIMATION_RATIO
slider = Slider(slider_ax, "Speed", slider_min, slider_max, valinit=slider_init)


def update_speed(val):
    global SIMULATION_ANIMATION_RATIO
    # animation.event_source.interval = slider.val
    SIMULATION_ANIMATION_RATIO = int(slider.val)


slider.on_changed(update_speed)


plt.show()
