from abc import ABC, abstractmethod
from copy import copy
# import time
# from joblib import Parallel, delayed
import numpy as np


DEPTH = 3
PARAMETER_POSIBLE_VALUES_NUMBER = 3
STATE_SPACE_LENGTH = PARAMETER_POSIBLE_VALUES_NUMBER**DEPTH

STATE_SPACE = np.array([[0, 0, 0],
                        [0, 0, 1],
                        [0, 0, 2],
                        [0, 1, 0],
                        [0, 1, 1],
                        [0, 1, 2],
                        [0, 2, 0],
                        [0, 2, 1],
                        [0, 2, 2],
                        [1, 0, 0],
                        [1, 0, 1],
                        [1, 0, 2],
                        [1, 1, 0],
                        [1, 1, 1],
                        [1, 1, 2],
                        [1, 2, 0],
                        [1, 2, 1],
                        [1, 2, 2],
                        [2, 0, 0],
                        [2, 0, 1],
                        [2, 0, 2],
                        [2, 1, 0],
                        [2, 1, 1],
                        [2, 1, 2],
                        [2, 2, 0],
                        [2, 2, 1],
                        [2, 2, 2]])


class MultiCell():
    def __init__(self, init_state: np.ndarray):
        # self.rendering_duration = rendering_duration
        # self.n_jobs = -1
        (self.height, self.width, self.depth) = init_state.shape
        assert self.depth == DEPTH
        self.set_state(init_state)
        self.__temperature = 0
        self.init_tables()
        
    def init_tables(self):
        self.__not_permitted_neighbors_table = []
        for h in range(self.height):
            not_permitted_neighbors_row = []
            for w in range(self.width):
                not_permitted_neighbors_row.append([])
            self.__not_permitted_neighbors_table.append(not_permitted_neighbors_row)
        
    @property
    def state(self) -> np.ndarray:
        return self.__state

    def set_state(self, state):
        self.__state = state
            
    def transition(self) -> None:
        next_state = copy(self.state)
        for h in range(self.height):
            for w in range(self.width):
                cell_next_state = STATE_SPACE[np.random.choice(STATE_SPACE_LENGTH)]
                if tuple(cell_next_state) not in self.__not_permitted_neighbors_table[h][w]:
                    assert tuple(cell_next_state) in [tuple(posible_state) for posible_state in STATE_SPACE]
                    next_state[h][w] = cell_next_state
        self.set_state(next_state)

    # def cell_step(self, cell_number):

    #     time.sleep(self.rendering_duration)
        
    #     (h, w) = cell_number // self.width, cell_number % self.width
    #     cell_next_state = STATE_SPACE[np.random.choice(STATE_SPACE_LENGTH)]
    #     if tuple(cell_next_state) not in self.__not_permitted_neighbors_table[h][w]:
    #         assert tuple(cell_next_state) in [tuple(posible_state) for posible_state in STATE_SPACE]
    #         return cell_next_state
    #     else:
    #         return self.state[h][w]
        
    # def transition_parallel(self) -> None:
    #     number_of_cells = self.height * self.width
    #     cells_states_list = Parallel(n_jobs=self.n_jobs)(delayed(self.cell_step)(cell_number) for cell_number in range(number_of_cells))

    #     next_state = copy(self.state)
        
    #     for cell_number in range(number_of_cells):
    #         (h, w) = cell_number // self.width, cell_number % self.width
    #         next_state[h][w] = cells_states_list[cell_number]
    #     self.set_state(next_state)

    def set_communication(self):
        for h in range(self.height):
            for w in range(self.width):
                self.__not_permitted_neighbors_table[h][w] = [tuple(not_permitted_state) 
                                                              for not_permitted_state in STATE_SPACE[:self.__temperature]]

    def temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        self.__temperature = min(max(temperature, 0), STATE_SPACE_LENGTH)
