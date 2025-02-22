import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import (
    Slider,
    Button,
    PolygonSelector,
    CheckButtons,
)  # , RadioButtons

from multi_agent_system import MultiCell, Simulation


# np.random.seed(2025)


# simulation constants
STEPS_IN_SIMULATION = 500
ROWS_NUMBER = 10
COLUMNS_NUMBER = 10
DEPTH = 3

TEMPERATURE_MIN = 0
TEMPERATURE_MAX = 27
TEMPERATURE_INIT = TEMPERATURE_MAX


# simulation core initialization
init_state = np.random.uniform(0, 1, (ROWS_NUMBER, COLUMNS_NUMBER, DEPTH))
multi_cell = MultiCell(init_state)
simulation = Simulation(multi_cell, STEPS_IN_SIMULATION)


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
FIGURE_SIZE = (5, 5)
SCENE_WIDTH = FIGURE_SIZE[1]
SCENE_HEIGHT = FIGURE_SIZE[0]
SCENE_SIZE = (SCENE_HEIGHT, SCENE_WIDTH)  # of multi agent system
SCATTER_SIZE = 500

# animation attributes
SIMULATION_NAME = "Synergistic Effect"
DURATION_OF_ANIMATION = STEPS_IN_SIMULATION / 10  # seconds
FRAMES_NUMBER = STEPS_IN_SIMULATION
DELAY_BETWEEN_FRAMES = 1000 * DURATION_OF_ANIMATION / FRAMES_NUMBER  # in milliseconds


# plot UI figure
fig_ui, [ax_bars, ax_slider, ax_button] = plt.subplots(nrows=3, ncols=1, figsize=(8, 5))


"""
fig_ui, ax_ui = plt.subplot_mosaic(
    [
        ["slider", "slider", "bars", "checks"],
        ["reset_slider", "reset_checks", "bars", "checks"],
    ],
    # width_ratios=[5, 1],
    layout="constrained",
)
# l, = ax['main'].plot(t, s0, lw=2, color='red')
"""

# plot Entropies bars
cells_entropies = simulation.group.entropies_of_cells()
cells_indexes = list(range(len(cells_entropies)))

scatter_bars = ax_bars.scatter(cells_indexes, cells_entropies, 10)
ax_bars.set_xticks(list(range(0, len(cells_entropies), 10)))
ax_bars.set_yticks([0, 1, 2, 3])
# ax_bars.set_aspect(30)
ax_bars.set_xlim(0, 100)
ax_bars.set_ylim(0, 3)
ax_bars.set(xlabel="cell", ylabel="entropy")
ax_bars.set_title("Entropies of Cells")

axcolor = "lightgoldenrodyellow"

# plot Slider
# ax_slider.set_aspect(30)
# ax_slider = plt.axes([0.25, 0.07, 0.65, 0.03], facecolor=axcolor)
slider_temperature = Slider(
    ax_slider,  # ax_ui["slider"],
    "# permited \n states",  # engagement; Cohesion
    TEMPERATURE_MIN,
    TEMPERATURE_MAX,
    valinit=TEMPERATURE_INIT,
    color=axcolor,
)


def update(val):
    number_of_permitted_states = slider_temperature.val
    simulation.group.set_number_of_permitted_states(number_of_permitted_states)

    scatter_bars_coords = []
    entropies_of_cells = simulation.group.entropies_of_cells()
    for cell_index, entropy in enumerate(entropies_of_cells):
        scatter_bars_coords.append([cell_index, entropy])
    scatter_bars.set_offsets(scatter_bars_coords)


slider_temperature.on_changed(update)

# plot Button reset_slider
# ax_button.set_aspect(30)
# ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
button_reset_slider = Button(
    ax_button, "Reset", hovercolor="0.975"  # ax_ui["reset_slider"],
)


def reset(event):
    slider_temperature.reset()


button_reset_slider.on_clicked(reset)

"""
TODO add new tools (mayby slyders for individual entropies)

# plot Button reset_checks
button_reset_checks = Button(
    ax_ui["reset_checks"], "reset_checks", hovercolor="0.975"
)

# plot Entropies bars
entropies_bars = ax_ui["bars"].plot()

# plot check boxes
check_boxes = PolygonSelector(ax_ui["checks"])
"""

fig_ui.show()


# plot animation figure
fig_animation, ax_scatter = plt.subplots(figsize=FIGURE_SIZE)
fig_animation.suptitle(SIMULATION_NAME, fontsize=14)

# plot scatter
ax_scatter.set_xticks([])
ax_scatter.set_yticks([])
ax_scatter.set_aspect("equal")
ax_scatter.set_xlim(-SCENE_WIDTH / 2, SCENE_WIDTH / 2)
ax_scatter.set_ylim(-SCENE_HEIGHT / 2, SCENE_HEIGHT / 2)

scatter_cells = ax_scatter.scatter([], [], SCATTER_SIZE)


# setup animation and run
def init_plot():
    coordinates, colors = scatter_representation_of_system_state(
        simulation.group.state, SCENE_WIDTH, SCENE_HEIGHT, SCATTER_SIZE
    )
    scatter_cells.set_offsets(coordinates)
    scatter_cells.set_color(colors)
    return (scatter_cells,)


def update_plot(frame):
    _ = next(simulation)  # here the simulation step heppens
    coordinates, colors = scatter_representation_of_system_state(
        simulation.group.state, SCENE_WIDTH, SCENE_HEIGHT, SCATTER_SIZE
    )
    scatter_cells.set_offsets(coordinates)
    scatter_cells.set_color(colors)
    return (scatter_cells,)


animation = FuncAnimation(
    fig=fig_animation,
    func=update_plot,
    frames=FRAMES_NUMBER,
    init_func=init_plot,
    blit=True,
    interval=DELAY_BETWEEN_FRAMES,
    repeat=False,
    # save_count=FRAMES_NUMBER
)

fig_animation.show()
