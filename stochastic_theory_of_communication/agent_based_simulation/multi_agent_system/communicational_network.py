"""
https://youtu.be/Ecqff-9Upjw?feature=shared

probability distribution for connection qualities modeling. metrics of communication
graf fundamentals

for this communicationsl network

for communication modelling and how does order emerges in it throuh the critical point
(phase) transition (bifurcation)
"""

from typing import List
from copy import copy
import numpy as np


class ProbabilityDistribution: ...


class Node:

    def __init__(self): ...

    @property
    def state(self) -> np.ndarray:
        return self.__state

    def output_(self) -> np.ndarray:
        return self.__output

    def entropy(self):
        return ...

    def neighbourhood_size(self) -> int:
        return ...

    def step(self, input_): ...

    """
    def neighbors_ids(self) -> List[int]:
        return self.__neighbors_ids
    
    def set_state_space_size(self, state_space_size: int):
        assert 1 <= state_space_size <= Cell.STATE_SPACE_SIZE
        self.__state_space_size = state_space_size

    def set_neighbors(self, neighbors_ids: List[int]):
        self.__neighbors_ids = neighbors_ids
        if self.id_ in self.__neighbors_ids:
            self.__neighbors_ids.remove(self.id_)
    """


class Group(Node):

    def __init__(self, init_state):
        super().__init__(self, init_state)

        ...

    @property
    def state(self) -> np.ndarray:
        return self.__state

    def output_(self) -> np.ndarray: ...

    def entropies_of_cells(self):
        return ...

    def entropy_additive(self): ...

    def entropy_join(self):  # synergistic
        ...

    def clustering_coefficient(self) -> float:
        return ...

    def communication_efficiency(self) -> float:
        """
        avg pathlength between to nodes among all pairs

        """
        return ...

    def set_state(self, state):
        self.__state = state

    def neighbourhood_size_distribution(self) -> ProbabilityDistribution:
        return ...

    def step(self, input_): ...

    def set_communication_by_probability_distribution(self): ...

    """
    def set_cells_state_space_size(self, state_space_size):
        state_space_size = int(state_space_size)
        state_space_size = max(state_space_size, 1)
        state_space_size = min(state_space_size, Cell.STATE_SPACE_SIZE)
        for cell in self.__cells:
            cell.set_state_space_size(state_space_size)
            
    def __set_cells(self):
        self.__cells = []
        for h in range(self.height):
            for w in range(self.width):
                cell_state = self.state[h][w]
                self.__cells.append(Cell(id_=self.width * h + w, init_state=cell_state))
                
    @property
    def number_of_permitted_states(self):
        # TODO this is not interesting parameter. must remake to connections
        return self.__number_of_permitted_states
    """
