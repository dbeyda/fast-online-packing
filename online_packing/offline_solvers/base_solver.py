from abc import ABC, abstractmethod
from typing import Union, List


class BaseSolver(ABC):
    _size: int
    _values: List[List[Union[float, int]]]
    _costs: List[List[List[Union[float, int]]]]
    _options_per_instant: int
    _cost_dimension: int

    def __init__(self, values: List[List[Union[float, int]]],
                 costs: List[List[List[Union[float, int]]]],
                 capacity: float):
        self._size = len(values)
        self._options_per_instant = len(values[0]) if len(values) else 0
        self._cost_dimension = len(costs[0][0]) if len(costs) and len(costs[0]) else 0
        self._values = values
        self._costs = costs
        self._capacity = capacity

    @abstractmethod
    def solve(self) -> None:
        pass

    @abstractmethod
    def print_result(self) -> None:
        pass
