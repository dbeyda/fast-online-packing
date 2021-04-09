from dataclasses import dataclass, field
from typing import List, Any, Union


def nested_list_initializer():
    a: List[Any] = list()
    a[0] = list()
    return a


@dataclass
class PackingProblem:
    values: List[Any] = field(default_factory=list)
    costs: List[List[Any]] = field(default_factory=nested_list_initializer)
    capacity: Union[int, float] = 0
    packed_value: Union[int, float] = 0
    packed_costs_sum: List[Union[int, float]] = field(default_factory=list)
    cost_dimension: int = field(init=False)

    def __post_init__(self):
        self.cost_dimension = len(self.costs)
