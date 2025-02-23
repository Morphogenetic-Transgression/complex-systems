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

    def is_state_in_states(state: np.ndarray, states: List[np.ndarray]):
        for neighbor_state in states:
            if list(state) == list(neighbor_state):
                return True
        return False

    def __init__(self, id_: int, init_state: np.ndarray):
        self.id_ = id_
        self.__state = init_state
        self.__state_space_size = Cell.STATE_SPACE_SIZE
        self.__neighbors_ids = []
        self.__permitted_states_indexes = list(range(self.__state_space_size))
        self.max_entropy = self.entropy()

    @property
    def state(self) -> np.ndarray:
        return self.__state

    def entropy(self):
        return Cell.system_entropy(
            Cell.ALPHABET_SIZE, len(self.__permitted_states_indexes)
        )

    def neighbors_ids(self) -> List[int]:
        return self.__neighbors_ids

    def step(self, neighbors_states: List[np.ndarray]):
        self.__permitted_states_indexes = []
        for state_index in range(self.__state_space_size):
            if not Cell.is_state_in_states(
                Cell.STATE_SPACE[state_index], neighbors_states
            ):
                self.__permitted_states_indexes.append(state_index)
        if self.__permitted_states_indexes:
            self.__state = Cell.STATE_SPACE[
                np.random.choice(self.__permitted_states_indexes)
            ]

    def set_state_space_size(self, state_space_size: int):
        assert 1 <= state_space_size <= Cell.STATE_SPACE_SIZE
        self.__state_space_size = state_space_size

    def set_neighbors(self, neighbors_ids: List[int]):
        self.__neighbors_ids = neighbors_ids
        if self.id_ in self.__neighbors_ids:
            self.__neighbors_ids.remove(self.id_)


class MultiCell:
    def __init__(self, init_state: np.ndarray):
        self.set_state(init_state)
        (self.height, self.width, self.alphabet_size) = self.state.shape
        assert self.alphabet_size == Cell.ALPHABET_SIZE
        self.__set_cells()
        # self.set_number_of_permitted_states(Cell.STATE_SPACE_SIZE)

    def __set_cells(self):
        self.__cells = []
        for h in range(self.height):
            for w in range(self.width):
                cell_state = self.state[h][w]
                self.__cells.append(Cell(id_=self.width * h + w, init_state=cell_state))

    @property
    def state(self) -> np.ndarray:
        return self.__state

    """
    @property
    def number_of_permitted_states(self):
        # TODO this is not interesting parameter. must remake to connections
        return self.__number_of_permitted_states
    """

    def set_state(self, state):
        self.__state = state

    def set_cells_state_space_size(self, state_space_size):
        state_space_size = int(state_space_size)
        state_space_size = max(state_space_size, 1)
        state_space_size = min(state_space_size, Cell.STATE_SPACE_SIZE)
        for cell in self.__cells:
            cell.set_state_space_size(state_space_size)

    def entropies_of_cells(self):
        return [cell.entropy() for cell in self.__cells]

    def entropy_additive(self): ...

    def entropy_join(self):  # synergistic
        ...

    """
    def get_permitted_states_indexes(self, h, w) -> List[int]:
        permitted_states_indexes = list(range(self.number_of_permitted_states))
        return permitted_states_indexes
    """

    def step(self) -> None:
        next_state = copy(self.state)
        for h in range(self.height):
            for w in range(self.width):
                current_cell = self.__cells[self.width * h + w]
                neighbors_states = [
                    self.__cells[neighbor_id].state
                    for neighbor_id in current_cell.neighbors_ids()
                ]
                current_cell.step(neighbors_states)
                next_state[h][w] = current_cell.state
        self.set_state(next_state)

    def set_neighborhude(self, communication_table: np.ndarray):
        neighborhude = []
        for h in range(self.height):
            for w in range(self.width):
                if communication_table[h][w] == 1:
                    neighborhude.append(self.width * h + w)
        for cell_index in neighborhude:
            self.__cells[cell_index].set_neighbors(neighborhude)

    def reset_neighborhude(self):
        # TODO
        ...
