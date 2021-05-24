from abc import ABC, abstractmethod
from typing import Union, List


class BaseSolver(ABC):
    """Abstract class unifying methods for the offline solvers.

    Parameters
    ----------
    values : list of list of (int or float)
        A list of instants, where each instant contains is a list of the available values of that instant.
    costs : list of list of list of (int or float)
        A list of instants, where each instant is a list of options available, and each option
        is a list containing this option's costs for each dimension.
    capacity : float
        The capacity of each dimension (each dimension have the same capacity).

    Attributes
    ----------
    optimum_value : float or int
        The optimum value found for the LP problem.
    packed_items : list of int
        A list containing the indexes of the items chosen in each instant.
    packed_weight_sum : list of float
        A list containing the optimal solution's total cost for each dimension.

    Methods
    -------
    solve()
        Abstract method, should solve the LP problem.
    print_result()
        Prints a report containing the optimum solution and the total weights in each dimension.
    """
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
        """Abstract method that should solve the LP problem and set
        `optimum_value`, `packed_items` and `packed_weight_sum` attributes.
        """
        pass

    def print_result(self) -> None:
        """Prints a report containing the optimum solution
        and the total weights in each dimension
        """
        print(f"Total value = {self.optimum_value:.4f}")
        for dim in range(self._cost_dimension):
            print(
                f"\tTotal weight dim {dim}: {self.packed_weight_sum[dim]:.5f} / {self._capacity:.5f}")
