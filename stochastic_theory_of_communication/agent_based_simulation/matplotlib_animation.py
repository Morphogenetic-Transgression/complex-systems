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
STEPS_IN_SIMULATION = 5000
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


# ======================================================= plot UI figure
fig_ui, [ax_bars, ax_slider, ax_button] = plt.subplots(nrows=3, ncols=1, figsize=(5, 5))

# ======================================================= plot Entropies bars
cells_entropies = simulation.group.entropies_of_cells()
cells_indexes = list(range(len(cells_entropies)))

scatter_bars = ax_bars.scatter(cells_indexes, cells_entropies, 10)
ax_bars.set_xticks(list(range(0, len(cells_entropies), 10)))
ax_bars.set_yticks([0, 1, 2, 3])
ax_bars.set_xlim(0, 100)
ax_bars.set_ylim(0, 3)
ax_bars.set(xlabel="cell", ylabel="entropy")
ax_bars.set_title("Entropies of Cells")

axcolor = "lightgoldenrodyellow"

# ======================================================= plot Slider
slider_state_space_size = Slider(
    ax_slider,
    "State \n Space \n Size",  # engagement; Cohesion
    TEMPERATURE_MIN,
    TEMPERATURE_MAX,
    valinit=TEMPERATURE_INIT,
    color=axcolor,
)


def update(val):
    state_space_size = slider_state_space_size.val
    simulation.group.set_cells_state_space_size(state_space_size)

    scatter_bars_coords = []
    entropies_of_cells = simulation.group.entropies_of_cells()
    for cell_index, entropy in enumerate(entropies_of_cells):
        scatter_bars_coords.append([cell_index, entropy])
    scatter_bars.set_offsets(scatter_bars_coords)


slider_state_space_size.on_changed(update)

# ======================================================= plot Button reset_slider
button_reset_slider = Button(ax_button, "Reset", hovercolor="0.975")


def reset_slider(event):
    slider_state_space_size.reset()


button_reset_slider.on_clicked(reset_slider)

fig_ui.show()

# ======================================================= plot CheckButtons
CHECKBOXES_COLUMNS_NUMBER = COLUMNS_NUMBER
CHECKBOXES_ROWS_NUMBER = ROWS_NUMBER

fig_checkboxes, ax_checkboxes = plt.subplot_mosaic(
    [
        [f"checks_row_{i}" for i in range(CHECKBOXES_COLUMNS_NUMBER)],
        ["apply" for i in range(CHECKBOXES_COLUMNS_NUMBER)],
        ["clear" for i in range(CHECKBOXES_COLUMNS_NUMBER)],
    ],
    height_ratios=[5, 1, 1],
    layout="constrained",
    figsize=(5, 5),
)
fig_checkboxes.suptitle("Set Up Connections", fontsize=14)

# check_boxes
check_boxes = [
    CheckButtons(
        ax_checkboxes[f"checks_row_{i}"], labels=list(range(CHECKBOXES_ROWS_NUMBER))
    )
    for i in range(CHECKBOXES_COLUMNS_NUMBER)
]

# button_apply_check_boxes
button_apply_check_boxes = Button(
    ax_checkboxes["apply"], "Set as Neighbors", hovercolor="0.975"
)
# ax_checkboxes["apply"].set_aspect(1 / 40)


def apply_check_boxes(event):
    communication_table = np.zeros((ROWS_NUMBER, COLUMNS_NUMBER))
    for w in range(CHECKBOXES_COLUMNS_NUMBER):
        column_status = check_boxes[w].get_status()
        for h in range(CHECKBOXES_ROWS_NUMBER):
            if column_status[h]:
                communication_table[h][w] = 1
    print(communication_table)
    print()
    simulation.group.set_neighborhude(communication_table)

    # reset entropies
    scatter_bars_coords = []
    entropies_of_cells = simulation.group.entropies_of_cells()
    for cell_index, entropy in enumerate(entropies_of_cells):
        scatter_bars_coords.append([cell_index, entropy])
    scatter_bars.set_offsets(scatter_bars_coords)


button_apply_check_boxes.on_clicked(apply_check_boxes)


# button_reset_check_boxes
button_reset_check_boxes = Button(ax_checkboxes["clear"], "Clear", hovercolor="0.975")
# ax_checkboxes["clear"].set_aspect(1 / 40)


def reset_check_boxes(event):
    for w in range(CHECKBOXES_COLUMNS_NUMBER):
        check_boxes[w].clear()  # TODO clear is very slow
    simulation.group.reset_neighborhude()


button_reset_check_boxes.on_clicked(reset_check_boxes)


fig_checkboxes.show()


# ======================================================= plot animation figure
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
