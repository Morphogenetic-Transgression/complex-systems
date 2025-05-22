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
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def z_1(theta):
    z = np.exp(1j * theta)
    return z


def z_2(theta):
    z = np.exp(1j * theta) + np.exp(3 * 1j * theta)
    return z


def z_3(theta):
    z = np.exp(1j * theta) + np.exp(np.pi * 1j * theta)
    return z


class QuasiPeriodicSystem:

    def __init__(self, z, sampling_time, r_init=1, theta_init=0, omega_init=0):
        self.z = z
        self.sampling_time = sampling_time
        self.r = r_init
        self.theta = theta_init
        self.theta_prev = self.theta
        self.omega = omega_init

    @property
    def state(self) -> np.ndarray:
        z = self.z(self.theta)
        x = self.r * z.real
        y = self.r * z.imag
        return np.array([x, y])

    def cycles_number(self) -> int:
        return int(self.theta / (2 * np.pi))

    def step(self) -> None:
        self.theta += self.sampling_time * self.omega


class Torus:

    def __init__(self, sampling_time, r_init=1, theta_init=0, omega_init=0):
        self.sampling_time = sampling_time
        self.r = r_init
        self.theta = theta_init
        self.theta_prev = self.theta
        self.omega = omega_init

    @property
    def cos_theta(self) -> float:
        return np.cos(self.theta)

    @property
    def cos_pi_theta(self) -> float:
        return np.cos(np.pi * self.theta)

    @property
    def theta_(self) -> float:
        return self.theta % (2 * np.pi)

    @property
    def state(self) -> np.ndarray:
        return np.array([self.cos_theta, self.cos_pi_theta, self.theta_])

    def cycles_number(self) -> int:
        return int(self.theta / (2 * np.pi))

    def step(self) -> None:
        self.theta += self.sampling_time * self.omega


# constants
SAMPLING_TIME = 50e-3  # seconds in mechanical step of system
FPS = 200000
ANIMATION_DURATION = 1000  # seconds
FRAMES_NUMBER = int(ANIMATION_DURATION * FPS)
DELAY_BETWEEN_FRAMES_MILLISEC = 1000 / FPS  # in milliseconds

SURFACE_WIDTH = 10  # TODO rename
SURFACE_HEIGHT = 10

SIMULATION_NAME = r"Transcendentality of $\pi$ causes Quasiperiodicity"


# utilites
def axis_initialize(fig, index_, title, title_color=None):
    ax = fig.add_subplot(2, 2, index_)

    ax.set_title(title)
    if title_color:
        ax.set_title(title, color=title_color)
    ax.set_aspect("equal")
    ax.set_xlim(-SURFACE_WIDTH / 2, SURFACE_WIDTH / 2)
    ax.set_ylim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
    ax.set(xlabel=r"Re", ylabel=r"Im")
    ax.set_xticks([]),
    ax.set_yticks([])

    scatter_size = 10
    scatter = ax.scatter([], [], scatter_size)
    scatter.set_color("red")

    (trail,) = ax.plot([], [], "b-", lw=0.3)
    trail_x_data, trail_y_data = [], []

    text = None
    if index_ == 1:
        text = ax.text(-(SURFACE_HEIGHT / 2) * 0.92, (SURFACE_HEIGHT / 2) * 0.92, s="")

    return ax, text, scatter, trail, trail_x_data, trail_y_data


def axis_draw_dynamics(pis, text, scatter, trail, trail_x_data, trail_y_data):
    if text:
        text.set_text(f"cycles number: {pis.cycles_number()}")
    scatter.set_offsets(pis.state)
    trail_x_data.append(pis.state[0])
    trail_y_data.append(pis.state[1])
    trail.set_data(trail_x_data, trail_y_data)
    return text, scatter, trail, trail_x_data, trail_y_data


def axis_3d_initialize(fig, index_, title):
    ax = fig.add_subplot(2, 2, index_, projection="3d")

    ax.set_title(title)
    ax.set_aspect("equal")
    ax.set_xlim(-SURFACE_WIDTH / 2, SURFACE_WIDTH / 2)
    ax.set_ylim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
    ax.set_zlim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
    ax.set(
        xlabel=r"$\cos(\theta)$",
        ylabel=r"$\cos(\pi \cdot \theta)$",
        zlabel=r"$\theta$" + " mod " + r"$2 \cdot \pi$",
    )
    ax.set_xticks([]),
    ax.set_yticks([])
    ax.set_zticks([])

    (trail,) = ax.plot([], [], [], "b-", lw=0.5)

    trail_x_data = []
    trail_y_data = []
    trail_z_data = []  # Lists to store the trajectory

    return ax, trail, trail_x_data, trail_y_data, trail_z_data


def axis_3d_draw_dynamics(sys, trail, trail_x_data, trail_y_data, trail_z_data):

    cos_theta, cos_pi_theta, theta_ = sys.state

    trail_x_data.append(cos_theta)
    trail_y_data.append(cos_pi_theta)
    trail_z_data.append(theta_)

    trail.set_data(trail_x_data, trail_y_data)
    trail.set_3d_properties(trail_z_data)

    return trail, trail_x_data, trail_y_data, trail_z_data


omega_init = 1.6


# system init
pis_1 = QuasiPeriodicSystem(
    z=z_1,
    sampling_time=SAMPLING_TIME,
    r_init=SURFACE_WIDTH / 4.5,
    theta_init=0,
    omega_init=omega_init,
)

pis_2 = QuasiPeriodicSystem(
    z=z_2,
    sampling_time=SAMPLING_TIME,
    r_init=SURFACE_WIDTH / 4.5,
    theta_init=0,
    omega_init=omega_init,
)

pis_3 = QuasiPeriodicSystem(
    z=z_3,
    sampling_time=SAMPLING_TIME,
    r_init=SURFACE_WIDTH / 4.5,
    theta_init=0,
    omega_init=omega_init,
)

pis_3d = Torus(
    sampling_time=SAMPLING_TIME,
    r_init=SURFACE_WIDTH / 4.5,
    theta_init=0,
    omega_init=omega_init,
)


# plotting and animation
fig = plt.figure(figsize=(10, 10))


ax_1, text_1, scatter_1, trail_1, trail_x_data_1, trail_y_data_1 = axis_initialize(
    fig, 1, title=r"$z = e^{i \cdot \theta}$"
)
ax_2, text_2, scatter_2, trail_2, trail_x_data_2, trail_y_data_2 = axis_initialize(
    fig, 2, title=r"$z = e^{i \cdot \theta} + e^{3 \cdot i \cdot \theta}$"
)
ax_3, text_3, scatter_3, trail_3, trail_x_data_3, trail_y_data_3 = axis_initialize(
    fig,
    3,
    title=r"$z = e^{i \cdot \theta} + e^{\pi \cdot i \cdot \theta}$",
    title_color="r",
)

ax_3d, trail_3d, trail_x_data_3d, trail_y_data_3d, trail_z_data_3d = axis_3d_initialize(
    fig, 4, title="Non-self-intersecting Projection"
)


def update_plot(frame):

    global text_1, scatter_1, trail_1, trail_x_data_1, trail_y_data_1, text_2, scatter_2, trail_2, trail_x_data_2, trail_y_data_2, text_3, scatter_3, trail_3, trail_x_data_3, trail_y_data_3, trail_3d, trail_x_data_3d, trail_y_data_3d, trail_z_data_3d

    text_1, scatter_1, trail_1, trail_x_data_1, trail_y_data_1 = axis_draw_dynamics(
        pis_1, text_1, scatter_1, trail_1, trail_x_data_1, trail_y_data_1
    )

    text_2, scatter_2, trail_2, trail_x_data_2, trail_y_data_2 = axis_draw_dynamics(
        pis_2, text_2, scatter_2, trail_2, trail_x_data_2, trail_y_data_2
    )

    text_3, scatter_3, trail_3, trail_x_data_3, trail_y_data_3 = axis_draw_dynamics(
        pis_3, text_3, scatter_3, trail_3, trail_x_data_3, trail_y_data_3
    )

    trail_3d, trail_x_data_3d, trail_y_data_3d, trail_z_data_3d = axis_3d_draw_dynamics(
        pis_3d, trail_3d, trail_x_data_3d, trail_y_data_3d, trail_z_data_3d
    )

    pis_1.step()
    pis_2.step()
    pis_3.step()
    pis_3d.step()

    return (
        text_1,
        scatter_1,
        trail_1,
        # text_2,
        scatter_2,
        trail_2,
        # text_3,
        scatter_3,
        trail_3,
        trail_3d,
    )


animation = FuncAnimation(
    fig=fig,
    func=update_plot,
    frames=FRAMES_NUMBER,
    blit=True,
    interval=DELAY_BETWEEN_FRAMES_MILLISEC,
    repeat=False,
    save_count=FRAMES_NUMBER,
)

fig.suptitle(SIMULATION_NAME, fontsize=14)

plt.show()
