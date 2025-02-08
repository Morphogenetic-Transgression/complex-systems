


def cell_step(self, cell_number):

    time.sleep(self.rendering_duration)
    
    (h, w) = cell_number // self.width, cell_number % self.width
    cell_next_state = STATE_SPACE[np.random.choice(STATE_SPACE_LENGTH)]
    if tuple(cell_next_state) not in self.__not_permitted_neighbors_table[h][w]:
        assert tuple(cell_next_state) in [tuple(posible_state) for posible_state in STATE_SPACE]
        return cell_next_state
    else:
        return self.state[h][w]
    
    
def transition_parallel(self) -> None:
    number_of_cells = self.height * self.width
    cells_states_list = Parallel(n_jobs=self.n_jobs)(delayed(self.cell_step)(cell_number) for cell_number in range(number_of_cells))

    next_state = copy(self.state)
    
    for cell_number in range(number_of_cells):
        (h, w) = cell_number // self.width, cell_number % self.width
        next_state[h][w] = cells_states_list[cell_number]
    self.set_state(next_state)
    
