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
    def __init__(self, init_state: np.ndarray, depth, spherical: bool):
        # добавить параметр глубины. указывает 1, 4, 16, ... клеток в макроклетке
        # при переходе вся система итерирует состояние каждой макроклетки. состояния макроклеток могут зависеть друг от друга (связаны)
        # но походу и случайны. связанность уменьшает случайность. состояние макроклетки зависит от состояний других макроклеток. 
        # но начинается с гомогенных состояний для макроклеток. (это не обязательно. можно и начальное ссотояние указать для всего. 
        # главное параметр добавить)
        self.alphabet = np.array([0, 1])
        self.p = 1 / len(self.alphabet) # probability of "1"
        self.distribution = np.array([self.p, 1 - self.p])
        assert self.alphabet.shape == self.distribution.shape, "probability distribution over state space has incorrect shape"
        self.set_state(init_state)
        self.spherical = spherical
        self.macro_cells = None
        self.n, self.m = self.state.shape
        assert self.n == self.m
        self.depth = depth
        if self.depth > 0:
            self.macro_cells = []
            macro_cell_side = int(4**(self.depth/2))
            assert (self.n % macro_cell_side) == 0
            for i in range(int(self.n // macro_cell_side)):
                macro_cells_row = []
                for j in range(int(self.m // macro_cell_side)):
                    macro_cells_row.append(MultiAgent(init_state = self.state[i*macro_cell_side : (i+1)*macro_cell_side, 
                                                                              j*macro_cell_side : (j+1)*macro_cell_side],
                                                      depth=0,
                                                      spherical=self.spherical))
                self.macro_cells.append(macro_cells_row)
                    
            
        
    @property
    def state(self) -> np.ndarray:
        return self.__state

    @property
    def entropy_cell(self) -> float:
        # entropy of a single cell
        # return np.dot(self.distribution, -np.log2(self.distribution)) # == - p * log2(p) - (1-p) * log2(1-p) == 1/2 + 1/2 == 1, btw
        return 1. # what is equal to 1 bit

    @property
    def entropy_total(self) -> float:
        # sum of individual entropies of all cells
        return np.prod(self.state.shape) * self.entropy_cell # == just amount of bits (because of uniform distribution)

    @property
    def entropy_anal(self) -> float:
        # TODO analiticaly calculated joint entropy
        return ...

    @property
    def entropy_freq(self) -> float:
        # TODO calculated by frequency distribution
        return ...

    @property
    def entropy_slice_total(self) -> float:
        # TODO entropy of rectangle
        # а если там есть клетка, которая связана с не входящими в этот прямоугольник? ну и что?
        return ...

    @property
    def entropy_slice_joint(self) -> float:
        # TODO entropy of rectangle
        # а если там есть клетка, которая связана с не входящими в этот прямоугольник? ну и что?
        return ...

    def set_state(self, state: np.ndarray) -> None:
        self.__state = copy(state)
        
    def random_choice(self) -> np.ndarray:
        return np.random.choice(len(self.alphabet), self.state.shape)

    def transition(self) -> None:
        next_state = self.random_choice()
        if self.depth > 0:
            macro_cell_side = int(4**(self.depth/2))
            for i in range(int(self.n // macro_cell_side)):
                for j in range(int(self.m // macro_cell_side)):
                    self.macro_cells[i][j].transition() # TODO в перспективе можно передавать соседов
                    # TODO сейчас не связаны, но  если связаны, то их состояния зависят друг от друга
                    for k in range(macro_cell_side):
                        for l in range(macro_cell_side):
                            next_state[i*macro_cell_side : (i+1)*macro_cell_side, 
                                       j*macro_cell_side : (j+1)*macro_cell_side][k][l] = self.macro_cells[i][j].state[k][l]
        self.set_state(next_state)  


class MultiAgentGameLife(MultiAgent):
    def __init__(self, init_state: np.ndarray, spherical: bool):
        self.alphabet = np.array([0, 1])
        self.p = 1 / len(self.alphabet) # probability of "1"
        self.distribution = np.array([self.p, 1 - self.p])
        assert self.alphabet.shape == self.distribution.shape, "probability distribution over state space has incorrect shape"
        self.set_state(init_state)
        self.spherical = spherical
        
    @property
    def state(self) -> np.ndarray:
        return self.__state

    @property
    def entropy_cell(self) -> float:
        # entropy of a single cell
        # return np.dot(self.distribution, -np.log2(self.distribution)) # == - p * log2(p) - (1-p) * log2(1-p) == 1/2 + 1/2 == 1, btw
        return 1. # what is equal to 1 bit

    @property
    def entropy_total(self) -> float:
        # sum of individual entropies of all cells
        return np.prod(self.state.shape) * self.entropy_cell # == just amount of bits (because of uniform distribution)

    @property
    def entropy_anal(self) -> float:
        # TODO analiticaly calculated joint entropy
        return ...

    @property
    def entropy_freq(self) -> float:
        # TODO calculated by frequency distribution
        return ...

    @property
    def entropy_slice_total(self) -> float:
        # TODO entropy of rectangle
        # а если там есть клетка, которая связана с не входящими в этот прямоугольник? ну и что?
        return ...

    @property
    def entropy_slice_joint(self) -> float:
        # TODO entropy of rectangle
        # а если там есть клетка, которая связана с не входящими в этот прямоугольник? ну и что?
        return ...

    def set_state(self, state: np.ndarray) -> None:
        self.__state = copy(state)
        
    def random_choice(self) -> np.ndarray:
        return np.random.choice(len(self.alphabet), self.state.shape)

    def transition(self) -> None:
        # next_state = copy(self.state)
        # self.set_state(next_state)  
        self.transition_life_game()

    def map_life_game(self, current, neighbors: List) -> float:
        if (sum(neighbors) < 2) or (sum(neighbors) > 3):
            return 0
        else:
            if current == 0:
                if sum(neighbors) == 3:
                    return 1
            return current
            
    def transition_life_game(self) -> None:
        next_state = copy(self.state)
        n, m = self.state.shape
        if not self.spherical:
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
        
    
        
