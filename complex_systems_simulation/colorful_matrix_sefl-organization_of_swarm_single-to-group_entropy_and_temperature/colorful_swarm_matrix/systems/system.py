from abc import ABC, abstractmethod
from copy import copy
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


class MultiAgent():
    def __init__(self, init_state: np.ndarray):
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

    def set_communication(self):
        for h in range(self.height):
            for w in range(self.width):
                self.__not_permitted_neighbors_table[h][w] = [tuple(not_permitted_state) 
                                                              for not_permitted_state in STATE_SPACE[:self.__temperature]]

    def temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        self.__temperature = min(max(temperature, 0), STATE_SPACE_LENGTH)


