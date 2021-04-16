from abc import ABC, abstractmethod
from typing import Union, List


class BaseSolver(ABC):
    _size: int
    _values: List[List[Union[float, int]]]
    _costs: List[List[List[Union[float, int]]]]
    _options_per_instant: int
    _cost_dimension: int
    optimum_value: Union[float, int]
    packed_items: List[int]
    packed_weight_sum: List[float]

    def __init__(self, values: List[List[Union[float, int]]],
                 costs: List[List[List[Union[float, int]]]],
                 capacity: float):
        self._size = len(values)
        self._options_per_instant = len(values[0]) if len(values) else 0
        self._cost_dimension = len(costs[0][0]) if len(costs) and len(costs[0]) else 0
        self._values = values
        self._costs = costs
        self._capacity = capacity
        self.optimum_value = 0.0
        self.packed_items = list()
        self.packed_weight_sum = [0.0 for _ in range(self._cost_dimension)]

    @abstractmethod
    def solve(self) -> None:
        pass

    def print_result(self) -> None:
        print(f"Total value = {self.optimum_value:.4f}")
        for dim in range(self._cost_dimension):
            print(
                f"\tTotal weight dim {dim}: {self.packed_weight_sum[dim]:.5f} / {self._capacity:.5f}")
