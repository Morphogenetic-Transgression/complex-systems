import numpy as np


class InitialState:
    def __init__(self, rows_number, columns_number):
        self.alphabet_size = 2
        self.rows_number = rows_number
        self.columns_number = columns_number

    @property
    def zeros(self):
        return np.zeros((self.rows_number, self.columns_number))

    @property
    def random(self):
        return np.random.choice(self.alphabet_size, (self.rows_number, self.columns_number))

    @property
    def glider_gun(self):
        init_state = self.zeros
        cells = [(22, 8),
                 (12, 7),
                 (36, 7),
                 (17, 9),
                 (11, 8),
                 (1, 9),
                 (25, 4),
                 (2, 8),
                 (16, 7),
                 (25, 10),
                 (21, 6),
                 (23, 9),
                 (14, 6),
                 (36, 6),
                 (22, 7),
                 (14, 12),
                 (17, 8),
                 (11, 10),
                 (25, 9),
                 (35, 7),
                 (1, 8),
                 (18, 9),
                 (22, 6),
                 (21, 8),
                 (23, 5),
                 (12, 11),
                 (17, 10),
                 (11, 9),
                 (35, 6),
                 (25, 5),
                 (2, 9),
                 (13, 6),
                 (13, 12),
                 (15, 9),
                 (16, 11),
                 (21, 7)]
        for x, y in cells:
            init_state[y][x] = 1   
        return init_state
        














