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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button


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

    """
    @property
    def cos_theta(self) -> float:
        return np.cos(self.theta)

    @property
    def cos_pi_theta(self) -> float:
        return np.cos(np.pi * self.theta)

    @property
    def theta_(self) -> float:
        return self.theta % (2 * np.pi)
    """

    @property
    def state(self) -> np.ndarray:

        # return np.array([self.cos_theta, self.cos_pi_theta, self.theta_])

        R = 4
        r = 2
        u = self.theta
        v = self.theta * np.pi

        x = R * np.cos(u) + r * np.cos(v) * np.cos(u)

        y = R * np.sin(u) + r * np.cos(v) * np.sin(u)

        z = r * np.sin(v)

        return np.array([x, y, z])

    def cycles_number(self) -> int:
        return int(self.theta / (2 * np.pi))

    def step(self) -> None:
        self.theta += self.sampling_time * self.omega


# constants
SAMPLING_TIME = 0.05  # seconds in mechanical step of system
SIMULATION_DURATION = 10  # seconds of real system time
STEPS_IN_SIMULATION = np.arange(0, SIMULATION_DURATION, SAMPLING_TIME)
SKIP_N = 50  # animate every 5th step
FRAMES_NUMBER = range(0, len(STEPS_IN_SIMULATION), SKIP_N)
DELAY_BETWEEN_FRAMES_MILLISEC = 1  # each frame appears for 0.02 seconds on screen

SURFACE_WIDTH = 10  # TODO rename
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

    scatter_size = 10
    scatter = ax.scatter([], [], scatter_size)
    scatter.set_color("red")

    (trail,) = ax.plot([], [], "b-", lw=0.3)
    trail_x_data, trail_y_data = [], []

    text = None
    if index_ == 1:
        text = ax.text(-(SURFACE_HEIGHT / 2) * 0.92, (SURFACE_HEIGHT / 2) * 0.92, s="")

    return text, scatter, trail, trail_x_data, trail_y_data


def axis_draw_dynamics(pis, text, scatter, trail, trail_x_data, trail_y_data):
    if text:
        text.set_text(f"cycles number: {pis.cycles_number()}")
    scatter.set_offsets(pis.state)
    trail_x_data.append(pis.state[0])
    trail_y_data.append(pis.state[1])
    trail.set_data(trail_x_data, trail_y_data)
    return text, scatter, trail, trail_x_data, trail_y_data


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
        # xlabel=r"$\cos(\theta)$",
        # ylabel=r"$\cos(\pi \cdot \theta)$",
        # zlabel=r"$\theta$" + " mod " + r"$2 \cdot \pi$",
    )
    ax.set_xticks([]),
    ax.set_yticks([])
    ax.set_zticks([])

    (trail,) = ax.plot([], [], [], "b-", lw=0.5)

    trail_x_data = []
    trail_y_data = []
    trail_z_data = []  # Lists to store the trajectory

    return trail, trail_x_data, trail_y_data, trail_z_data


def axis_3d_draw_dynamics(sys, trail, trail_x_data, trail_y_data, trail_z_data):

    cos_theta, cos_pi_theta, theta_ = sys.state

    trail_x_data.append(cos_theta)
    trail_y_data.append(cos_pi_theta)
    trail_z_data.append(theta_)

    trail.set_data(trail_x_data, trail_y_data)
    trail.set_3d_properties(trail_z_data)

    return trail, trail_x_data, trail_y_data, trail_z_data


# system init

omega_init = 1.3

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


text_1, scatter_1, trail_1, trail_x_data_1, trail_y_data_1 = axis_initialize(
    ax1, 1, title=r"$z = e^{i \cdot \theta}$" + " (periodic)"
)
text_2, scatter_2, trail_2, trail_x_data_2, trail_y_data_2 = axis_initialize(
    ax2,
    2,
    title=r"$z = e^{i \cdot \theta} + e^{3 \cdot i \cdot \theta}$" + " (periodic)",
)
text_3, scatter_3, trail_3, trail_x_data_3, trail_y_data_3 = axis_initialize(
    ax3,
    3,
    title=r"$z = e^{i \cdot \theta} + e^{\pi \cdot i \cdot \theta}$"
    + " (quasi-periodic because of "
    + r"$\pi$)"
    + "\n The curve never closes.",
    title_color="r",
)

trail_3d, trail_x_data_3d, trail_y_data_3d, trail_z_data_3d = axis_3d_initialize(
    ax4,
    4,
    title="Phase Projection of "
    + r"$(e^{i \cdot \theta}, e^{\pi \cdot i \cdot \theta})$"
    + " embedded into "
    + r"$\mathbb{R}^3$"
    + ". Phase Trajectory does not intersect itself.",
)

# animation

paused = [True]  # mutable so it can be modified from nested scope


def update_plot(frame):

    global text_1, scatter_1, trail_1, trail_x_data_1, trail_y_data_1, text_2, scatter_2, trail_2, trail_x_data_2, trail_y_data_2, text_3, scatter_3, trail_3, trail_x_data_3, trail_y_data_3, trail_3d, trail_x_data_3d, trail_y_data_3d, trail_z_data_3d

    if not paused[0]:

        text_1, scatter_1, trail_1, trail_x_data_1, trail_y_data_1 = axis_draw_dynamics(
            pis_1, text_1, scatter_1, trail_1, trail_x_data_1, trail_y_data_1
        )

        text_2, scatter_2, trail_2, trail_x_data_2, trail_y_data_2 = axis_draw_dynamics(
            pis_2, text_2, scatter_2, trail_2, trail_x_data_2, trail_y_data_2
        )

        text_3, scatter_3, trail_3, trail_x_data_3, trail_y_data_3 = axis_draw_dynamics(
            pis_3, text_3, scatter_3, trail_3, trail_x_data_3, trail_y_data_3
        )

        trail_3d, trail_x_data_3d, trail_y_data_3d, trail_z_data_3d = (
            axis_3d_draw_dynamics(
                pis_3d, trail_3d, trail_x_data_3d, trail_y_data_3d, trail_z_data_3d
            )
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
    interval=DELAY_BETWEEN_FRAMES_MILLISEC,
    blit=True,
    # repeat=False,
    # save_count=FRAMES_NUMBER,
)


# Add pause/play button
button_ax = plt.axes([0.8, 0.025, 0.1, 0.04])  # x, y, width, height
button = Button(button_ax, "Play", hovercolor="0.975")


def toggle(event):
    paused[0] = not paused[0]
    button.label.set_text("Play" if paused[0] else "Pause")


button.on_clicked(toggle)


plt.show()
