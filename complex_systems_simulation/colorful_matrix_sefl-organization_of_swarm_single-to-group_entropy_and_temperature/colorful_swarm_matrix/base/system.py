from abc import ABC, abstractmethod
from typing import List, Tuple
from copy import deepcopy
import numpy as np


class State(ABC):

    @property
    def shape(self) -> Tuple[float]:
        ...

    @property
    def parameters_range(self) -> Tuple[float]:
        ...

    
class System(ABC):

    @property
    def state(self) -> np.ndarray:
        ...

    @abstractmethod
    def transition(self, *args, **kwargs) -> None:
        ...


class StateRGB250(State):
    depth = 3
    def __init__(self, state_np: np.ndarray):
        self.__shape = (StateRGB250.depth,)
        self.__parameters_range = (0, 1)
        assert state_np.shape == self.__shape
        assert all([self.parameters_range[0] <= p <= self.parameters_range[1] for p in state_np])
        self.__state_np = state_np

    def as_nparray(self) -> np.ndarray:
        return self.__state_np

    def as_tuple(self) -> Tuple[float]:
        return tuple(self.as_nparray())

    def as_rgb250(self) -> Tuple[int]:
        return tuple(np.round(self.as_nparray()*250).astype(int))

    @property
    def shape(self) -> Tuple[float]:
        return self.__shape

    @property
    def parameters_range(self) -> Tuple[float]:
        return self.__parameters_range
        

class Agent(System):
    def __init__(self, init_state: State):
        self.__state = init_state
        
    @property
    def state(self) -> State:
        return self.__state

    def choice_random_state(self) -> State: # infinite space of nature
        return StateRGB250(np.random.uniform(self.state.parameters_range[0], 
                                             self.state.parameters_range[1], 
                                             self.state.shape[0]))

    def calculate_next_state(self, not_permitted_states: List[State]): 
        # not general case but particular implementstion of map beatween current and next state
        self.__next_state = self.choice_random_state()
        if self.__next_state.as_rgb250 in [not_permitted_state.as_rgb250 for not_permitted_state in not_permitted_states]:
            self.__next_state = deepcopy(self.state)
        
    def transition(self) -> None:
        assert self.__next_state is not None, "calculate the next state befor calling transition"
        self.__state = self.__next_state
        
        
class MultiAgent(System):
    def __init__(self, init_state: np.ndarray):
        (self.height, self.width, self.depth) = init_state.shape
        assert self.depth == StateRGB250.depth
        self.__state = init_state
        self.initialize_the_group_of_agents()

    def initialize_the_group_of_agents(self):
        self.__agents_matrix = []
        for h in range(self.height):
            agents_row = []
            for w in range(self.width):
                state = StateRGB250(self.__state[h][w])
                agent = Agent(state)
                agents_row.append(agent)
            self.__agents_matrix.append(agents_row)
                
    def set_communication(self): # TODO set not_permitted_states
        ...
        
    @property
    def state(self) -> np.ndarray:
        return self.__state
            
    def transition(self) -> None:
        
        # calculate next state for each agent
        for h in range(self.height):
            for w in range(self.width):
                agent_not_permitted_states = []
                self.__agents_matrix[h][w].calculate_next_state(agent_not_permitted_states)
        
        # do trasition for each agent
        for h in range(self.height):
            for w in range(self.width):
                self.__agents_matrix[h][w].transition()

                self.__state[h][w] = self.__agents_matrix[h][w].state.as_nparray()
        










        
        
    
        
