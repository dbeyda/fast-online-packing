from typing import List, Union


class PackingProblem:
    capacity: Union[int, float, None] = None
    # internal use
    _packed_items: List[int] = list()
    _packed_value_sum: Union[int, float] = 0
    _packed_costs_sum: List[Union[int, float]] = list()
    _cost_dimension: int
    _options_per_instant: int
    _total_time: int
    # inputs seen in until current time
    # values: 1st index = day   //   2nd index = item value
    _available_values: List[List[Union[int, float]]] = list()
    # costs: 1st index = day   //   2nd index = item costs vector   //   3rd index = item cost dimension
    _available_costs: List[List[List[Union[int, float]]]] = list()

    def __init__(self, capacity: Union[float, int]):
        self._set_capacity(capacity)

    def _set_capacity(self, capacity: Union[float, int]):
        if capacity < 0 - 1e-6:
            raise Exception(f"Capacity must be >= 0 (tried setting to {capacity}).")
        elif self.capacity is not None:
            raise Exception(f"Capacity already set (capacity={self.capacity}).")
        else:
            self.capacity = capacity

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
            for cost in costs:
                if len(cost) != self._cost_dimension:
                    raise Exception("Received a cost vector with different dimension from previously seen.")

    def set_current_inputs(self, values: List[Union[int, float]],
                           costs: List[List[Union[int, float]]]) -> None:
        if len(self._packed_items) < len(self._available_values):
            raise Exception(
                "Tried to set next instant without choosing an option for the current instant.")
        self._validate_curr_inputs(values, costs)
        self._available_values.append(values)
        self._available_costs.append(costs)
        if len(self._available_values) == 1:
            self._options_per_instant = len(values)
            self._cost_dimension = len(costs[0])

    def pack(self, idx: int) -> Union[int, float]:
        if len(self._available_values) == len(self._packed_items):
            raise Exception(
                "Tried to pack an item twice in the same time instant. A new input should be set.")
        elif idx < 0 or idx > self._options_per_instant-1:
            raise Exception(f"Tried to pack item out of bounds. Available indexes to pack are [0, ..., \
                {self._options_per_instant-1}].")

        # pack chosen item
        self._packed_items.append(idx)
        for dim in range(self._cost_dimension):
            self._packed_costs_sum[dim] += self._available_costs[-1][idx][dim]
        self._packed_value_sum += self._available_values[-1][idx]
        return self._packed_value_sum
