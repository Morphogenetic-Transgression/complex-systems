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
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class PiSystem:

    def __init__(self, sampling_time, r_init=1, theta_init=0, omega_init=0):
        self.sampling_time = sampling_time
        self.r = r_init
        self.theta = theta_init
        self.theta_prev = self.theta
        self.omega = omega_init

    def z(self, theta):
        z = np.exp(1j * theta) + np.exp(np.pi * 1j * theta)  # * self.r
        return z

    @property
    def state(self) -> np.ndarray:
        # circle
        # x = self.r * np.cos(self.theta)
        # y = self.r * np.sin(self.theta)

        # double pendulum
        z = self.z(self.theta)
        x = self.r * z.real
        y = self.r * z.imag

        return np.array([x, y])

    @property
    def cos_theta(self) -> float:
        return np.cos(self.theta)

    @property
    def cos_pi_theta(self) -> float:
        return np.cos(np.pi * self.theta)

    @property
    def theta_(self) -> float:
        return self.theta % (2 * np.pi)

    def step(self) -> None:
        self.theta_prev = self.theta
        self.theta = self.theta + self.sampling_time * self.omega

    def control_velocity(self, omega) -> None:
        self.omega = omega

    @property
    def phi(self):

        # numerical
        z_prev = z = self.z(self.theta_prev)
        x_prev = self.r * z_prev.real
        y_prev = self.r * z_prev.imag

        z = self.z(self.theta)
        x = self.r * z.real
        y = self.r * z.imag

        x_dot = (x_prev - x) / self.sampling_time
        y_dot = (y_prev - y) / self.sampling_time

        phi_numer = np.arctan(y_dot / x_dot)

        # analitical
        x_dot_anal = -(
            np.sin(self.theta) + np.pi * np.sin(np.pi * self.theta)
        )  # *theta_dot
        y_dot_anal = np.cos(self.theta) + np.pi * np.cos(
            np.pi * self.theta
        )  # *theta_dot
        phi_anal = np.arctan(y_dot_anal / x_dot_anal)

        # print((phi_numer, phi_anal))

        return phi_anal


SAMPLING_TIME = 50e-3  # seconds in mechanical step of system
FPS = 1000
ANIMATION_DURATION = 20  # seconds
FRAMES_NUMBER = int(ANIMATION_DURATION * FPS)
DELAY_BETWEEN_FRAMES_MILLISEC = 1000 / FPS  # in milliseconds

SURFACE_WIDTH = 10  # TODO rename
SURFACE_HEIGHT = 10

SIMULATION_NAME = "Chaos in pi"


# system init
pis = PiSystem(
    sampling_time=SAMPLING_TIME,
    r_init=SURFACE_WIDTH / 4.5,
    theta_init=0,
    omega_init=1,
)


# plotting and animation
scatter_mech_size = 20
scatter_phase_size = 20

# fig, (ax1, _) = plt.subplots(figsize=(20, 10), ncols=2)
fig = plt.figure(figsize=(20, 10))

ax1 = fig.add_subplot(1, 2, 1)

# ax 1 for Mechanical Space
ax1.set_title("Position in Mechanical Space")
ax1.set_aspect("equal")
ax1.set_xlim(-SURFACE_WIDTH / 2, SURFACE_WIDTH / 2)
ax1.set_ylim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
ax1.set(xlabel=f"x", ylabel=f"y")
ax1.set_xticks([]),
ax1.set_yticks([])

scatter_mech = ax1.scatter([], [], scatter_mech_size)
scatter_mech.set_color("red")

(trail_mech,) = ax1.plot([], [], "b-", lw=0.3)  # the trajectory trail_mech
trail_mech_x_data, trail_mech_y_data = [], []  # Lists to store the trajectory

ax1.annotate(
    "",
    xytext=(pis.state[0] + 1 / (2**0.5), pis.state[1] + 1 / (2**0.5)),
    xy=(pis.state[0], pis.state[1]),
    arrowprops=dict(arrowstyle="->"),
)


# ax 2 for Phase Space
ax2 = fig.add_subplot(1, 2, 2, projection="3d")

ax2.set_title("Position Phase Space")
# ax2.set_aspect("equal")
ax2.set_xlim(-SURFACE_WIDTH / 2, SURFACE_WIDTH / 2)
ax2.set_ylim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
ax2.set_zlim(-SURFACE_HEIGHT / 2, SURFACE_HEIGHT / 2)
ax2.set(xlabel="x", ylabel="y", zlabel="phi")
ax2.set_xticks([]),
ax2.set_yticks([])
ax2.set_zticks([])

(trail_phase,) = ax2.plot([], [], [], "b-", lw=0.5)  # the trajectory trail_mech

"""
scatter_phase = ax2.scatter([], [], [], scatter_phase_size)
scatter_phase.set_color("red")
trail_phase = ax2.plot([], [], [], "b-", lw=0.4)  # the trajectory trail_mech
"""
trail_phase_x_data = []
trail_phase_y_data = []
trail_phase_phi_data = []  # Lists to store the trajectory


def init_plot():

    scatter_mech.set_offsets(pis.state)
    trail_mech_x_data.append(pis.state[0])
    trail_mech_y_data.append(pis.state[1])
    trail_mech.set_data(trail_mech_x_data, trail_mech_y_data)

    trail_phase_x_data.append(pis.cos_theta)
    trail_phase_y_data.append(pis.cos_pi_theta)
    trail_phase_phi_data.append(pis.theta_)

    trail_phase.set_data(trail_phase_x_data, trail_phase_y_data)
    trail_phase.set_3d_properties(trail_phase_phi_data)

    # ax2.collections.clear()
    # ax2.scatter([pis.state[0]], [pis.state[1]], [pis.phi], color="red")

    return (scatter_mech, trail_mech, trail_phase)


def update_plot(frame):

    pis.step()

    scatter_mech.set_offsets(pis.state)
    trail_mech_x_data.append(pis.state[0])
    trail_mech_y_data.append(pis.state[1])
    trail_mech.set_data(trail_mech_x_data, trail_mech_y_data)

    trail_phase_x_data.append(pis.cos_theta)
    trail_phase_y_data.append(pis.cos_pi_theta)
    trail_phase_phi_data.append(pis.theta_)

    trail_phase.set_data(trail_phase_x_data, trail_phase_y_data)
    trail_phase.set_3d_properties(trail_phase_phi_data)

    # ax2.collections.clear()
    # ax2.scatter([pis.state[0]], [pis.state[1]], [pis.phi], color="red")

    return (scatter_mech, trail_mech, trail_phase)


animation = FuncAnimation(
    fig=fig,
    func=update_plot,
    frames=FRAMES_NUMBER,
    init_func=init_plot,
    blit=True,
    interval=DELAY_BETWEEN_FRAMES_MILLISEC,
    repeat=False,
    save_count=FRAMES_NUMBER,
)

fig.suptitle(SIMULATION_NAME, fontsize=14)

plt.show()
