import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button  # , RadioButtons

from multi_agent_system import MultiCell, Simulation


# np.random.seed(2025)


# simulation constants
class SimulationConfig:
    STEPS_IN_SIMULATION = 500
    ROWS_NUMBER = 10
    COLUMNS_NUMBER = 10
    DEPTH = 3

    TEMPERATURE_MIN = 0
    TEMPERATURE_MAX = 27
    TEMPERATURE_INIT = TEMPERATURE_MIN


# simulation core initialization
def init_simulation(
    rows_number, columns_number, depth, steps_in_simulation
) -> Simulation:
    init_state = np.random.uniform(0, 1, (rows_number, columns_number, depth))
    multi_cell = MultiCell(init_state)
    simulation = Simulation(multi_cell, steps_in_simulation)
    return simulation


def scatter_representation_of_system_state(
    multi_cell_state, scene_width, scene_height, scatter_size
):
    height, width, alphabet_size = multi_cell_state.shape
    dots_margin_x = scene_width / width
    dots_margin_y = scene_height / height
    coordinates = []
    colors = []
    for y in range(height):
        for x in range(width):
            coordinates.append(
                [
                    (x - width / 2 + 1 / 2) * dots_margin_x,
                    (y - height / 2 + 1 / 2) * dots_margin_y,
                ]
            )
            colors.append(multi_cell_state[x][y])
    coordinates = np.array(coordinates)
    colors = np.array(colors)
    return coordinates, colors


# visualization initialization
class VisualizationConfig:
    FIGURE_SIZE = (8, 8)
    SCENE_WIDTH = FIGURE_SIZE[1]
    SCENE_HEIGHT = FIGURE_SIZE[0]
    SCENE_SIZE = (SCENE_HEIGHT, SCENE_WIDTH)  # of multi agent system
    SCATTER_SIZE = 50

    # animation attributes
    SIMULATION_NAME = "Cohesion of Cells"
    DURATION_OF_ANIMATION = SimulationConfig.STEPS_IN_SIMULATION / 10  # seconds
    FRAMES_NUMBER = SimulationConfig.STEPS_IN_SIMULATION
    DELAY_BETWEEN_FRAMES = (
        1000 * DURATION_OF_ANIMATION / FRAMES_NUMBER
    )  # in milliseconds


fig, ax = plt.subplots(figsize=FIGURE_SIZE)
fig.suptitle(SIMULATION_NAME, fontsize=14)

# plot particles
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.set_xlim(-SCENE_WIDTH / 2, SCENE_WIDTH / 2)
ax.set_ylim(-SCENE_HEIGHT / 2, SCENE_HEIGHT / 2)

scatter = ax.scatter([], [], SCATTER_SIZE)

# plot Slider
axcolor = "lightgoldenrodyellow"
ax_slider = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor=axcolor)
slider_temperature = Slider(
    ax_slider,
    "Cohesion",  # engagement
    TEMPERATURE_MIN,
    TEMPERATURE_MAX,
    valinit=TEMPERATURE_INIT,
)


def update(val):
    temperature = slider_temperature.val
    simulation.group.set_temperature(temperature)
    simulation.group.set_communication_rules()


slider_temperature.on_changed(update)

# plot Button
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(ax_reset, "Reset", color=axcolor, hovercolor="0.975")


def reset(event):
    slider_temperature.reset()


button_reset.on_clicked(reset)

# plot text (simulation steps left)
# ax_text = plt.axes([0.1, 0.025, 0.1, 0.04])


# setup animation and run
def init_plot():
    coordinates, colors = scatter_representation_of_system_state(
        simulation.group.state, SCENE_WIDTH, SCENE_HEIGHT, SCATTER_SIZE
    )
    scatter.set_offsets(coordinates)
    scatter.set_color(colors)
    return (scatter,)


def update_plot(frame):
    step_number = next(simulation)  # here the simulation step heppens
    coordinates, colors = scatter_representation_of_system_state(
        simulation.group.state, SCENE_WIDTH, SCENE_HEIGHT, SCATTER_SIZE
    )
    scatter.set_offsets(coordinates)
    scatter.set_color(colors)
    # print(step_number)  # TODO render on step number on figure
    # print()
    return (scatter,)


animation = FuncAnimation(
    fig=fig,
    func=update_plot,
    frames=FRAMES_NUMBER,
    init_func=init_plot,
    blit=True,
    interval=DELAY_BETWEEN_FRAMES,
    repeat=False,
    # save_count=FRAMES_NUMBER
)

plt.show()
