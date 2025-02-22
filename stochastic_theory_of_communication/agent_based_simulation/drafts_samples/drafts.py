def cell_step(self, cell_number):

    time.sleep(self.rendering_duration)

    (h, w) = cell_number // self.width, cell_number % self.width
    cell_next_state = STATE_SPACE[np.random.choice(STATE_SPACE_LENGTH)]
    if tuple(cell_next_state) not in self.__not_permitted_neighbors_table[h][w]:
        assert tuple(cell_next_state) in [
            tuple(posible_state) for posible_state in STATE_SPACE
        ]
        return cell_next_state
    else:
        return self.state[h][w]


def transition_parallel(self) -> None:
    number_of_cells = self.height * self.width
    cells_states_list = Parallel(n_jobs=self.n_jobs)(
        delayed(self.cell_step)(cell_number) for cell_number in range(number_of_cells)
    )

    next_state = copy(self.state)

    for cell_number in range(number_of_cells):
        (h, w) = cell_number // self.width, cell_number % self.width
        next_state[h][w] = cells_states_list[cell_number]
    self.set_state(next_state)


def step_of_cell(self, cell_current_state, not_permitted_neighbors):
    cell_next_state = Cell.choice_random_state()
    if tuple(cell_next_state) not in not_permitted_neighbors:
        assert tuple(cell_next_state) in [
            tuple(posible_state) for posible_state in Cell.STATE_SPACE
        ]  # TODO remove assert
        return cell_next_state
    return cell_current_state


def __init_communicational_properties(self):
    # maybe here will be some additional initialisations
    init_number_of_permitted_states = 0  # TODO add to arguments
    self.set_number_of_permitted_states(
        number_of_permitted_states=init_number_of_permitted_states
    )
    self.__not_permitted_neighbors_table = []  # TODO add init table to arguments (?)
    for h in range(self.height):
        not_permitted_neighbors_row = []
        for w in range(self.width):
            not_permitted_neighbors_row.append([])
        self.__not_permitted_neighbors_table.append(not_permitted_neighbors_row)


def set_communication_rules(self):
    for h in range(self.height):
        for w in range(self.width):
            self.__not_permitted_neighbors_table[h][w] = [
                tuple(not_permitted_state)
                for not_permitted_state in Cell.STATE_SPACE[
                    : self.__number_of_permitted_states
                ]
            ]
