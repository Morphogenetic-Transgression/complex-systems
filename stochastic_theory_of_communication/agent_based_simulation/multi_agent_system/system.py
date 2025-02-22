from typing import List
from copy import copy
import numpy as np


class Cell:

    ALPHABET_SIZE = 3
    NUMBER_OF_PARAMETERS = 3
    STATE_SHAPE = (NUMBER_OF_PARAMETERS,)
    STATE_SPACE_SIZE = ALPHABET_SIZE**NUMBER_OF_PARAMETERS
    # TODO automatic construction of STATE_SPACE in constructor
    STATE_SPACE = (
        np.array(
            [
                [0, 0, 0],
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
                [2, 2, 2],
            ]
        )
        / ALPHABET_SIZE
    )

    def system_entropy(alphabet_size, state_space_size):  # TODO or '-' ?
        entropy = np.log2(state_space_size) / np.log2(
            alphabet_size
        )  # = log_{alphabet_size}(state_space_size)
        # entropy = NUMBER_OF_PARAMETERS = log_{ALPHABET_SIZE}(STATE_SPACE_SIZE)
        return float(entropy)

    def __init__(self, init_state: np.ndarray):
        self.__state = init_state
        self.__permitted_states_indexes = list(range(Cell.STATE_SPACE_SIZE))
        self.max_entropy = self.entropy()

    @property
    def state(self) -> np.ndarray:
        return self.__state

    def step(
        self, permitted_states_indexes: List[int]
    ):  # from the univers (dependance on the cosmos)
        # return Cell.STATE_SPACE[np.random.choice(Cell.STATE_SPACE_SIZE)]
        self.__permitted_states_indexes = permitted_states_indexes
        if self.__permitted_states_indexes:
            self.__state = Cell.STATE_SPACE[
                np.random.choice(self.__permitted_states_indexes)
            ]

    def entropy(self):
        return Cell.system_entropy(
            Cell.ALPHABET_SIZE, len(self.__permitted_states_indexes)
        )


class MultiCell:
    def __init__(self, init_state: np.ndarray):
        self.set_state(init_state)
        (self.height, self.width, self.alphabet_size) = self.state.shape
        assert self.alphabet_size == Cell.ALPHABET_SIZE
        self.__set_cells()
        self.set_number_of_permitted_states(Cell.STATE_SPACE_SIZE)

    def __set_cells(self):
        self.__cells = []
        for h in range(self.height):
            for w in range(self.width):
                cell_state = self.state[h][w]
                self.__cells.append(Cell(cell_state))

    @property
    def state(self) -> np.ndarray:
        return self.__state

    @property
    def number_of_permitted_states(self):
        # TODO this is not interesting parameter. must remake to connections
        return self.__number_of_permitted_states

    def set_state(self, state):
        self.__state = state

    def set_number_of_permitted_states(self, number_of_permitted_states):
        number_of_permitted_states = int(number_of_permitted_states)
        number_of_permitted_states = max(number_of_permitted_states, 1)
        self.__number_of_permitted_states = min(
            number_of_permitted_states, Cell.STATE_SPACE_SIZE
        )

    def entropies_of_cells(self):
        return [cell.entropy() for cell in self.__cells]

    def entropy_additive(self): ...

    def entropy_join(self):  # synergistic
        ...

    def get_permitted_states_indexes(self, h, w) -> List[int]:
        permitted_states_indexes = list(range(self.number_of_permitted_states))
        return permitted_states_indexes

    def step(self) -> None:
        next_state = copy(self.state)
        for h in range(self.height):
            for w in range(self.width):
                permitted_states_indexes = self.get_permitted_states_indexes(h, w)
                self.__cells[self.width * h + w].step(permitted_states_indexes)
                next_state[h][w] = self.__cells[self.width * h + w].state
        self.set_state(next_state)
