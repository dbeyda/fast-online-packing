from dataclasses import dataclass, field
from typing import List, Any, Union


def nested_list_initializer():
    a: List[Any] = list()
    a[0] = list()
    return a


def triple_nested_list_initializer():
    a: List[Any] = list()
    a[0] = list()
    a[0][0] = list()
    return a


@dataclass
class PackingProblem:
    # values: 1st index = day   //   2nd index = item value
    values: List[List[Any]] = field(default_factory=nested_list_initializer)
    # costs: 1st index = day   //   2nd index = item costs vector   //   3rd index = item cost dimension
    costs: List[List[List[Any]]] = field(default_factory=triple_nested_list_initializer)
    capacity: Union[int, float] = 0
    packed_value: Union[int, float] = 0
    packed_costs_sum: List[Union[int, float]] = field(default_factory=list)
    cost_dimension: int = field(init=False)
    itens_per_instant: int = field(init=False)
    instants: int = field(init=False)

    def __post_init__(self):
        self.instants = len(self.costs)
        if not self.instants:
            raise Exception("[Error] Creating packing problem with 0 days!!")
        elif len(self.values[0]) == 0:
            raise Exception("[Error] Creating instance with 0 items in each day!!")
        self.cost_dimension = len(self.costs[0][0])
        self.itens_per_instant = len(self.values[0])
