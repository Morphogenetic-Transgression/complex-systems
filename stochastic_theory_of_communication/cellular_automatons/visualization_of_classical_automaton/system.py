from abc import ABC, abstractmethod
from typing import List
from copy import copy
import numpy as np


class System(ABC):

    @property
    def state(self) -> np.ndarray:
        ...

    def transition(self, *args, **kwargs) -> None:
        ...


class MultiAgent(System):
    def __init__(self, init_state: np.ndarray, finite: bool):
        self.alphabet = [0, 1]
        self.set_state(init_state)
        self.finite = finite
        # self.life_rule_dict = {'0000': 0,
        #                  '0001': 1,
        #                  '0010': 1,
        #                  '0011': 1,
        #                  '0100': 0,
        #                  '0101': 1,
        #                  '0110': 1,
        #                  '0111': 0,
        #                  '1000': 0,
        #                  '1001': 0,
        #                  '1010': 0,
        #                  '1011': 0,
        #                  '1100': 0,
        #                  '1101': 0,
        #                  '1110': 0,
        #                  '1111': 0} 
        # self.rule_dict = {'000': 0,
        #                   '001': 1,
        #                   '010': 1,
        #                   '011': 1,
        #                   '100': 0,
        #                   '101': 1,
        #                   '110': 1,
        #                   '111': 0} 
        # self.rule_dict = {'000': 0,
        #                   '001': 1,
        #                   '010': 0,
        #                   '011': 1,
        #                   '100': 1,
        #                   '101': 0,
        #                   '110': 1,
        #                   '111': 0} 
        
    @property
    def state(self) -> np.ndarray:
        return self.__state

    def set_state(self, state: np.ndarray) -> None:
        self.__state = state
        
    def random_choice(self) -> np.ndarray:
        return np.random.choice(len(self.alphabet), self.state.shape)

    def map_life_game(self, current, neighbors: List) -> float:
        if (sum(neighbors) < 2) or (sum(neighbors) > 3):
            return 0
        else:
            if current == 0:
                if sum(neighbors) == 3:
                    return 1
            return current
            
    def transition(self) -> None:
        next_state = copy(self.state)
        n, m = self.state.shape
        if self.finite:
            for i in range(1, n-1):
                for j in range(1, m-1):
                    r = self.state[i][j+1]
                    rt = self.state[i-1][j+1]
                    t = self.state[i-1][j]
                    lt = self.state[i-1][j-1]
                    l = self.state[i][j-1]
                    lb = self.state[i+1][j-1]
                    b = self.state[i+1][j]
                    rb = self.state[i+1][j+1]
                    current = self.state[i][j]
                    neighbors = [r, rt, t, lt, l, lb, b, rb]
                    next_state[i][j] = self.map_life_game(current, neighbors)
        else:
            for i in range(n):
                for j in range(m):
                    r = self.state[i][(j+1) % m]
                    rt = self.state[(i-1) % n][(j+1) % m]
                    t = self.state[(i-1) % n][j]
                    lt = self.state[(i-1) % n][(j-1) % m]
                    l = self.state[i][(j-1) % m]
                    lb = self.state[(i+1) % n][(j-1) % m]
                    b = self.state[(i+1) % n][j]
                    rb = self.state[(i+1) % n][(j+1) % m]
                    current = self.state[i][j]
                    neighbors = [r, rt, t, lt, l, lb, b, rb]
                    next_state[i][j] = self.map_life_game(current, neighbors)
        self.set_state(next_state)   
        
    
        
