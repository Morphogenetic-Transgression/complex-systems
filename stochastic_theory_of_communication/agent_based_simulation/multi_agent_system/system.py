from copy import copy
import numpy as np


class Cell:
    ALPHABET_SIZE = 3
    NUMBER_OF_PARAMETERS = 3
    STATE_SHAPE = (NUMBER_OF_PARAMETERS, )
    STATE_SPACE_SIZE = ALPHABET_SIZE ** NUMBER_OF_PARAMETERS
    # TODO automatic construction of STATE_SPACE in constructor
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
                            [2, 2, 2]]) / ALPHABET_SIZE

    def choice_random_state():  # from the univers (dependance on the cosmos)
        return Cell.STATE_SPACE[np.random.choice(Cell.STATE_SPACE_SIZE)]
    
    def entropy():
        ...


class MultiCell():
    def __init__(self, init_state: np.ndarray):
        self.set_state(init_state)
        (self.height, self.width, self.alphabet_size) = self.state.shape
        assert self.alphabet_size == Cell.ALPHABET_SIZE
        self.number_of_agent = self.height * self.width
        self.__init_communicational_properties()  # init_temperature, init_not_permitted_neighbors_table

    @property
    def state(self) -> np.ndarray:
        return self.__state

    @property
    def temperature(self):
        return self.__temperature
    
    def entropy_additive(self):
        ...
        
    def entropy_join(self): # synergistic
        ...

    def step_of_cell(self, cell_current_state, not_permitted_neighbors):
        cell_next_state = Cell.choice_random_state()
        if tuple(cell_next_state) not in not_permitted_neighbors:
            assert tuple(cell_next_state) in [tuple(posible_state)
                                              for posible_state in Cell.STATE_SPACE]  # TODO remove assert
            return cell_next_state
        return cell_current_state

    def step(self) -> None:
        next_state = copy(self.state)
        for h in range(self.height):
            for w in range(self.width):
                next_state[h][w] = self.step_of_cell(cell_current_state=next_state[h][w],  # because it has been already copyed
                                                     not_permitted_neighbors=self.__not_permitted_neighbors_table[h][w])
        self.set_state(next_state)

    def set_state(self, state):
        self.__state = state

    def __init_communicational_properties(self):
        # maybe here will be some additional initialisations
        init_temperature = 0  # TODO add to arguments
        self.set_temperature(temperature=init_temperature)
        self.__not_permitted_neighbors_table = []  # TODO add init table to arguments (?)
        for h in range(self.height):
            not_permitted_neighbors_row = []
            for w in range(self.width):
                not_permitted_neighbors_row.append([])
            self.__not_permitted_neighbors_table.append(not_permitted_neighbors_row)

    def set_temperature(self, temperature):
        temperature = int(temperature)
        temperature = max(temperature, 0)
        self.__temperature = min(temperature, Cell.STATE_SPACE_SIZE)

    def set_communication_rules(self):
        for h in range(self.height):
            for w in range(self.width):
                self.__not_permitted_neighbors_table[h][w] = [tuple(not_permitted_state)
                                                              for not_permitted_state in Cell.STATE_SPACE[:self.__temperature]]
