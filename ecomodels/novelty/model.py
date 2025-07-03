from abc import ABC, abstractmethod


class EnergySource(ABC):

    @abstractmethod
    def discharge(self, energy_amount: float) -> float: ...


class EnergyConsumer(ABC):

    @abstractmethod
    def charge(self, energy_amount: float) -> float: ...


class Sun(EnergySource):

    def __init__(self, capacity, discharge_min, discharge_max, efficiency):
        self.capacity = capacity
        self.discharge_min = discharge_min
        self.discharge_max = discharge_max
        self.efficiency = efficiency

    def discharge(self, energy_amount: float) -> float:
        energy_amount = energy_amount * self.efficiency
        energy_amount = min(self.discharge_max, max(self.discharge_min, energy_amount))
        self.capacity -= energy_amount
        return energy_amount


class Earth(EnergySource, EnergyConsumer):
    """
    Earth without art is just 'Eh'

    dispel - рассеивать
    exploit - использовать, употреблять

    reframing of the second law is therefore that work necessarily
    means turning high-quality energy into lower-quality energy
    """

    def __init__(self, capacity, discharge_min, discharge_max, efficiency):
        self.capacity = capacity
        self.discharge_min = discharge_min
        self.discharge_max = discharge_max
        self.efficiency = efficiency

    def discharge(self, energy_amount: float) -> float:
        energy_amount = energy_amount * self.efficiency
        energy_amount = min(self.discharge_max, max(self.discharge_min, energy_amount))
        self.capacity -= energy_amount
        return energy_amount

    def charge(self, energy_amount: float) -> float:
        energy_amount = energy_amount * self.efficiency
        energy_amount = min(self.charge_max, max(self.charge_min, energy_amount))
        self.capacity += energy_amount
        return energy_amount
