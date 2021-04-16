from enum import Enum, auto
from typing import List, Union
import copy


class PackingProblem:
    class State(Enum):
        RUNNING = auto()
        FINISHED = auto()

    _capacity: Union[int, float] = -1
    # internal use
    _packed_items: List[int] = list()
    _packed_value_sum: Union[int, float]
    _packed_costs_sum: List[Union[int, float]]
    _cost_dimension: int
    _options_per_instant: int
    # inputs seen in until current time
    # values: 1st index = day   //   2nd index = item value
    _available_values: List[List[Union[int, float]]] = list()
    # costs: 1st index = day   //   2nd index = item costs vector   //   3rd index = item cost dimension
    _available_costs: List[List[List[Union[int, float]]]] = list()
    _state: State

    def __init__(self, capacity: Union[float, int], cost_dimension: int):
        self._packed_value_sum = 0.0
        self._state = PackingProblem.State.RUNNING
        self._set_capacity(capacity)
        self._set_cost_dimension(cost_dimension)

    @property
    def waiting_for_input(self) -> bool:
        return len(self._available_values) == len(self._packed_items)

    def _set_cost_dimension(self, cost_dimension: int):
        if cost_dimension <= 0:
            raise Exception("cost_dimension has to be greater than 0")
        self._cost_dimension = cost_dimension

    def _set_capacity(self, capacity: Union[float, int]):
        if capacity < 0 - 1e-6:
            raise Exception(f"Capacity must be >= 0 (tried setting to {capacity}).")
        elif self._capacity >= 0-1e-6:
            raise Exception(f"Capacity already set (capacity={self._capacity}).")
        else:
            self._capacity = capacity

    def get_capacity(self):
        return self._capacity

    def _validate_curr_inputs(self,
                              values: List[Union[int, float]],
                              costs: List[List[Union[int, float]]]) -> None:
        if len(values) != len(costs):
            raise Exception("len(values) != len(costs)")
        # validate values between 0 and 1:
        for v in values:
            if v < 0.0 - 1e-6 or v > 1 + 1e-6:
                raise Exception(
                    "Option values must be in range [0, 1].")
        for option in costs:
            if len(option) != self._cost_dimension:
                raise Exception("Received a cost vector with different dimension from previously seen.")
            for cost in option:
                if cost < 0 - 1e-6 or cost > 1 + 1e-6:
                    raise Exception("All option costs must in range [0, 1].")
        # validate number of options and cost-dimensions match previously seen:
        if len(self._available_values) > 0:
            if len(values) != self._options_per_instant:
                raise Exception(
                    "Number of available options in values in different from previously seen options.")
            if len(costs) != self._options_per_instant:
                raise Exception(
                    "Number of available options in costs is different from previously seen options.")

    def set_current_inputs(self, values: List[Union[int, float]],
                           costs: List[List[Union[int, float]]]) -> None:
        # TODO add State to the packing problem instance
        # so that when its finished, we can set_current_inputs
        # multiple times at the end
        if self._state is PackingProblem.State.RUNNING \
                and len(self._packed_items) < len(self._available_values):
            raise Exception(
                "Tried to set next instant without choosing an option for the current instant.")
        self._validate_curr_inputs(values, costs)
        self._available_values.append(values)
        self._available_costs.append(costs)
        if len(self._available_values) == 1:
            self._options_per_instant = len(values)
            self._packed_costs_sum = [0.0 for _ in range(self._cost_dimension)]

    def item_fits(self, idx: int) -> bool:
        for dim in range(self._cost_dimension):
            if self._available_costs[-1][idx][dim] + self._packed_costs_sum[dim] > self._capacity - 1e-6:
                return False
        return True

    def pack(self, idx: int) -> Union[int, float]:
        if self._state is PackingProblem.State.FINISHED:
            raise Exception(
                "Packing already finished. You may not continue to pack after packing was ended.")
        if len(self._available_values) == len(self._packed_items):
            raise Exception(
                "Packing already made. Currently waiting for the next input.")
        elif idx < 0 or idx > self._options_per_instant-1:
            raise Exception(f"Tried to pack item out of bounds. Available indexes to pack are [0, ..., \
                {self._options_per_instant-1}].")

        # pack chosen item
        if self.item_fits(idx):
            self._packed_items.append(idx)
            for dim in range(self._cost_dimension):
                self._packed_costs_sum[dim] += self._available_costs[-1][idx][dim]
            self._packed_value_sum += self._available_values[-1][idx]
            return self._packed_value_sum
        else:
            raise Exception("Tried to pack an item that exceeds capacity in some dimension")

    def end_packing(self):
        if self._state is PackingProblem.State.RUNNING:
            self._state = PackingProblem.State.FINISHED
        else:
            raise Exception("Problem state is already FINISHED.")

    def get_available_values(self):
        return copy.deepcopy(self._available_values)

    def get_available_costs(self):
        return copy.deepcopy(self._available_costs)

    def get_state(self):
        return self._state

    def get_cost_dimension(self):
        return self._cost_dimension
