"""This module encapsulates and formalizes all aspects
and rules of the Online Packing Problem.

For each instant, the algorithm receives k options of items, each one with a reward and a cost-vector.
The algorithm chooses which option to pack, and then waits until receiving the options for
the next instant. The algorithm can also choose to pack no items at a given instant. Also, it cannot
pack any item that that causes a violation of the capacity constraint in some dimension of the cost-vector.
"""
from typing import List, Union
import copy
from fast_online_packing.item import Item


class PackingProblem:
    """Class that enforces all aspects of the
    online packing problem.

    This class is statefull, meaning it carries the current state
    of the game, and some methods depend on that state.

    Parameters
    ----------
    capacity : float or int
        The maximum ocupation for the problem (it is the same for every cost dimension).
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
    get_capacity()
        Get capacity of the problem instance.
    get_available_values()
        Get the value of the items that are available for the current instant.
    get_available_costs()
        Get the cost-vectors of the items that are available for the current instant.
    cost_dimension
        Get the dimension of the cost vectors.
    """
    # TODO: document items_per_instant property

    _capacity: float
    _packed_items: List[int]
    _packed_rewards_sum: float
    _packed_costs_sum: List[float]
    _cost_dimension: int
    _items_per_instant: int
    # revealed_instants: inputs seen in until current time
    # 1st index = instant   //   2nd index = item
    _revealed_instants: List[List[Item]]

    def __init__(self, capacity: Union[float, int], cost_dimension: int):
        self._packed_rewards_sum = 0.0
        self._capacity = -1
        self._set_capacity(capacity)
        self._set_cost_dimension(cost_dimension)
        self._packed_items = list()
        self._items_per_instant = 0
        self._revealed_instants = list()

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
        if capacity < 0:
            raise Exception(f"Capacity must be >= 0 (tried setting to {capacity}).")
        elif self._capacity >= 0:
            raise Exception(f"Capacity already set (capacity={self._capacity}).")
        else:
            self._capacity = float(capacity)

    @property
    def capacity(self) -> float:
        """Get the problem capacity.

        Returns
        -------
        int or float
            Previously set problem capacity.
        """
        return self._capacity

    @property
    def items_per_instant(self) -> int:
        """Get the number of available items per instant.

        Returns
        -------
        int
            Number of available items per instant.
        """
        return self._items_per_instant

    @property
    def packed_rewards_sum(self) -> float:
        return self._packed_rewards_sum

    @property
    def packed_costs_sum(self) -> List[float]:
        return self._packed_costs_sum

    # TODO move item validation to Item class
    def _validate_curr_inputs(self, items: List[Item]) -> None:
        if self._items_per_instant and (len(items) != self._items_per_instant):
            raise Exception(
                f"Error: algorithm started with {self._items_per_instant} items per instant,\
                 but received {len(items)}.")
        for item in items:
            # validate rewards between 0 and 1:
            if item.reward < 0 or item.reward > 1:
                raise Exception("Error: item's rewards must be in the range [0, 1].")
            if item.cost_dim != self._cost_dimension:
                raise Exception("Error: received an item with a different cost dimension.")
            for c in item.costs:
                if c < 0 or c > 1:
                    raise Exception("Error: item's costs must be in range range [0, 1].")

    def set_current_inputs(self, items: List[Item]) -> None:
        if len(self._packed_items) < len(self._revealed_instants):
            raise Exception(
                "Error: tried to set next instant's items without picking an item for the current instant.")
        self._validate_curr_inputs(items)
        self._revealed_instants.append(items)
        if len(self._revealed_instants) == 1:
            self._items_per_instant = len(items)
            self._packed_costs_sum = [0.0 for _ in range(self._cost_dimension)]

    def item_fits(self, idx: int) -> bool:
        """Checks that item with index `idx`from current instant fits the capacity constriants.

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
        item = self._revealed_instants[-1][idx]
        for j in range(self._cost_dimension):
            if item.costs[j] + self._packed_costs_sum[j] > self._capacity:
                return False
        return True

    def pack(self, idx: int) -> float:
        """Pack item of index `idx`, from the currently available.

        Parameters
        ----------
        idx : int
            Index of the item to pack.

        Returns
        -------
        float
            Sum of rewards of the items packed so far.

        Raises
        ------
        Exception
            An item was already packed for the current instant.
        Exception
            Index for the item out of bounds.
        Exception
            Chosen item  exceed capacity in some dimension.
        """
        if len(self._revealed_instants) == len(self._packed_items):
            raise Exception(
                "Error: already packed an item for the current instant. You must reveal the next instant in\
                     order to continue packing.")
        elif idx < -1 or idx > self._items_per_instant-1:
            raise Exception(
                f"Error: tried to pack item of index {idx} which is out of bounds. Available indexes to pack are [0, ..., \
                {self._items_per_instant-1}] or -1 to pack no items.")

        # pack chosen item
        if idx == -1:
            self._packed_items.append(idx)
            return self._packed_rewards_sum
        elif self.item_fits(idx):
            self._packed_items.append(idx)
            for j in range(self._cost_dimension):
                self._packed_costs_sum[j] += self._revealed_instants[-1][idx].costs[j]
            self._packed_rewards_sum += self._revealed_instants[-1][idx].reward
            return self._packed_rewards_sum
        else:
            raise Exception("Error: tried to pack an item that exceeds capacity in some dimension.")

    def get_available_values(self) -> List[List[float]]:
        """Get values of all the available items for past and current instants.

        Returns
        -------
        list of list of float
            List contianing, for each instant, a list with the values of the available items for \
            that instant.
        """
        return [
            [item.reward for item in instant]
            for instant in self._revealed_instants
        ]

    def get_available_costs(self) -> List[List[List[Union[int, float]]]]:
        """Get costs of all the available items for past and current instants.

        Returns
        -------
        list of list of list of float
            List contianing, for each instant, a list with the cost vectors of the available items for \
            that instant.
        """
        return [
            [item.costs for item in instant]
            for instant in self._revealed_instants
        ]

    def get_revealed_instants(self) -> List[List[Item]]:
        return copy.deepcopy(self._revealed_instants)

    @property
    def cost_dimension(self):
        """Get the dimension of the cost vectors.

        Returns
        -------
        int
            The dimension of the cost vectors.
        """
        return self._cost_dimension
