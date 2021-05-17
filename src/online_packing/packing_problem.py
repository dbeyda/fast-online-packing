"""This module encapsulates and formalizes all aspects
and rules of the Online Packing Problem.

For each instant, the algorithm receives k options of items, each one with a value and a cost-vector.
The algorithm chooses which option to pack, and then waits until receiving the options for
the next instant. The algorithm can also choose to pack no items at a given instant. Also, it may not
pack any item that that causes a violation of the capacity constraint in some dimension.
"""
from typing import List, Union
import copy


class PackingProblem:
    """Class that enforces all aspects of the
    online packing problem.

    This class is statefull, meaning it carries the current state
    of the game, and some methods depend on that state.

    Parameters
    ----------
    capacity : float or int
        The capacity for the problem (same in every dimension).
    cost_dimension : int
        The dimension of the cost vector.

    Methods
    -------
    set_current_inputs(values, costs)
        Set items' values and costs for the current instant.
    item_fits(idx)
        Checks if current instant's item of index `idx` fits in capacity constraints.
    pack(idx)
        Pack current instant's item of index `idx`.
    end_packing()
        Ends the packing phase.
    get_capacity()
        Get capacity of the problem instance.
    get_options_per_instant()
        Get the number of available items in each instant.
    get_available_values()
        Get the value of the items that are available for the current instant.
    get_available_costs()
        Get the cost of the items that are available for the current instant.
    get_cost_dimension()
        Get the dimension of the cost vectors.
    """

    _capacity: Union[int, float]
    _packed_items: List[int]
    _packed_value_sum: Union[int, float]
    _packed_costs_sum: List[Union[int, float]]
    _cost_dimension: int
    _options_per_instant: int
    # inputs seen in until current time
    # values: 1st index = day   //   2nd index = item value
    _available_values: List[List[Union[int, float]]]
    # costs: 1st index = day   //   2nd index = item costs vector   //   3rd index = item cost dimension
    _available_costs: List[List[List[Union[int, float]]]]

    def __init__(self, capacity: Union[float, int], cost_dimension: int):
        self._packed_value_sum = 0.0
        self._capacity = -1
        self._set_capacity(capacity)
        self._set_cost_dimension(cost_dimension)
        self._available_values = list()
        self._available_costs = list()
        self._packed_items = list()

    def _set_cost_dimension(self, cost_dimension: int) -> None:
        """Validates cost dimension and sets cost dimension.

        Parameters
        ----------
        cost_dimension : int
            The dimension of the cost vectors.

        Raises
        ------
        Exception
            If `cost_dimension` is lower than 1.
        """
        if cost_dimension <= 0:
            raise Exception("cost_dimension has to be greater than 0")
        self._cost_dimension = cost_dimension

    def _set_capacity(self, capacity: Union[float, int]):
        """Validates and sets capacity for the problem.

        Parameters
        ----------
        capacity : float or int
            The capacity of each dimension (they must be the same).

        Raises
        -------
        Exception
            If capacity already set.
        Exception
            If capacity is negative.
        """
        if capacity < 0 - 1e-6:
            raise Exception(f"Capacity must be >= 0 (tried setting to {capacity}).")
        elif self._capacity >= 0-1e-6:
            raise Exception(f"Capacity already set (capacity={self._capacity}).")
        else:
            self._capacity = capacity

    def get_capacity(self) -> Union[int, float]:
        """Get the problem capacity.

        Returns
        -------
        int or float
            Previously set problem capacity.
        """
        return self._capacity

    def get_options_per_instant(self) -> int:
        """Get the number of available items per instant.

        Returns
        -------
        int
            Number of available items per instant.
        """
        return self._options_per_instant

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
        if len(self._packed_items) < len(self._available_values):
            raise Exception(
                "Tried to set next instant without choosing an option for the current instant.")
        self._validate_curr_inputs(values, costs)
        self._available_values.append(values)
        self._available_costs.append(costs)
        if len(self._available_values) == 1:
            self._options_per_instant = len(values)
            self._packed_costs_sum = [0.0 for _ in range(self._cost_dimension)]

    def item_fits(self, idx: int) -> bool:
        """Checks that currently available item of index `idx` fits the capacity constriants.

        Parameters
        ----------
        idx : int
            Index of the item to be verified.

        Returns
        -------
        bool
            True if the item fits the constraints, False otherwise.
        """
        if idx == -1:
            return True
        for dim in range(self._cost_dimension):
            if self._available_costs[-1][idx][dim] + self._packed_costs_sum[dim] > self._capacity + 1e-6:
                return False
        return True

    def pack(self, idx: int) -> Union[int, float]:
        """Pack item of index `idx`, from the currently available.

        Parameters
        ----------
        idx : int
            Index of the item to pack.

        Returns
        -------
        int or float
            Total value of the packed items so far.

        Raises
        ------
        Exception
            An item was already packed for the current instant.
        Exception
            Index for the item out of bounds.
        Exception
            Chosen item  exceed capacity in some dimension.
        """
        if len(self._available_values) == len(self._packed_items):
            raise Exception(
                "Packing already made. Currently waiting for the next input.")
        elif idx < -1 or idx > self._options_per_instant-1:
            raise Exception(f"Tried to pack item out of bounds. Available indexes to pack are [0, ..., \
                {self._options_per_instant-1}] or -1 to pack no items.")

        # pack chosen item
        if idx == -1:
            self._packed_items.append(idx)
            return self._packed_value_sum
        elif self.item_fits(idx):
            self._packed_items.append(idx)
            for dim in range(self._cost_dimension):
                self._packed_costs_sum[dim] += self._available_costs[-1][idx][dim]
            self._packed_value_sum += self._available_values[-1][idx]
            return self._packed_value_sum
        else:
            raise Exception("Tried to pack an item that exceeds capacity in some dimension")

    def get_available_values(self) -> List[List[Union[int, float]]]:
        """Get values of all the available items for past and current instants.

        Returns
        -------
        list of list of (int or float)
            List contianing, for each instant, a list with the values of the available items for \
            that instant.
        """
        return copy.deepcopy(self._available_values)

    def get_available_costs(self) -> List[List[List[Union[int, float]]]]:
        """Get costs of all the available items for past and current instants.

        Returns
        -------
        list of list of list of (int or float)
            List contianing, for each instant, a list with the cost vectors of the available items for \
            that instant.
        """
        return copy.deepcopy(self._available_costs)

    def get_cost_dimension(self):
        """Get the dimension of the cost vectors.

        Returns
        -------
        int
            The dimension of the cost vectors.
        """
        return self._cost_dimension
