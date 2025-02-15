from typing import Iterator
import numpy as np
from .system import MultiCell


class Simulation(Iterator):
    def __init__(self, group: MultiCell, steps_number: int):
        self.group = group
        self.steps_number = steps_number
        self.step_number = 0

    def __next__(self) -> np.ndarray:
        self.group.step()
        self.step_number += 1
        return self.step_number

    def __iter__(self) -> Iterator:
        return self
