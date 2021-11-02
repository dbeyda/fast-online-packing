"""This module contains an algorithm to solve the Online Packing Problem.

Notes
-----
The algorithm implemented here to solve the online packing problem
is described in [1]_, on section 6, as Algorithm 6.1. It uses the
MWU (Multiplicative Weights Update) method, as described in
[2]_, and Integer/Linear prorgamming solvers. Hence the `Mwu-Max`
and the `Offline Solvers` modules.

References
----------
.. [1] Agrawal, Shipra & Devanur, Nikhil. (2014). Fast Algorithms for Online Stochastic \
Convex Programming. Proceedings of the Annual ACM-SIAM Symposium on Discrete Algorithms. \
2015. 10.1137/1.9781611973730.93.

.. [2] Arora, Sanjeev & Hazan, Elad & Kale, Satyen. (2012). The Multiplicative Weights \
Update Method: a Meta Algorithm and Applications. Theory of Computing [electronic only]. \
8. 10.4086/toc.2012.v008a006.
"""

from math import log, sqrt, ceil
from typing import List, Union, Type
import random
from fast_online_packing.mwu_max import MwuMax
from operator import itemgetter
from fast_online_packing import helper
from fast_online_packing.offline_solvers.base_solver import BaseSolver
from fast_online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from fast_online_packing.item import Item
from fast_online_packing.base_online_solver import BaseOnlineSolver


class OnlineSolver(BaseOnlineSolver):
    """Solves the Online Packing Problem.

    Parameters
    ----------
    cost_dimension : int
        Dimension of the cost vectors to be used.
    total_time : int
        Total number of instants.
    capacity : float
        Capacity restriction of the problem instance.
    e : float or None, default=None
        Epsilon parameter to be used in the algorithm. If none is given, \
            a theorical optimum epsilon is set.
    solver_cls : Type[BaseSolver]
        Offline solver to be used.

    Attributes
    ----------
    p : PackingProblem
        Packing Problem instance, that holds and enforces all problem-related aspects.
    e : float
        Epsilon parameter used in the algorithm.
    mwu : MwuMax
        MWU instance.
    z : Union[float, None]
        Algorithm calculated parameter Z.
    delta : float
        Decimal fraction of instants used to estimate Z.
    total_time : int
        Total number of instants in the algorithm.
    current_time : int
        Count of the instant the algorithm currently is. 0-indexed.
    optimum_value : float
        Sum of the values of the items packed in the optimal solution (solving offline).
    cost_dimension : int
        Property that gets the dimension of the problem instance's cost vectors.

    Methods
    -------
    print_params()
        Print parameters used in the algorithm.
    pack_one(available_values, available_costs)
        Choose one of the given items to pack on the current instant.
    compute_optimum()
        Solves the offline problem for the previously set instants, \
            in order to find the optimum solution.
    print_result()
        Print a results report.
    get_premises_min()
        Gets the minimum value of the capacity and optimum-value-sum so that \
            premises and theoric guarantees are valid.
    respect_premises()
        Informs if the algorithm is in agreement with the theoric premises.
    """

    e: float
    mwu: MwuMax
    z: Union[float, None]
    delta: float

    def __init__(self, cost_dimension: int, total_time: int, capacity: float, e: Union[float, None] = None,
                 solver_cls: Type[BaseSolver] = PythonMIPSolver):

        super().__init__(cost_dimension, total_time, capacity, e)
        self.z = None
        e_2 = self.e * self.e
        self.delta = 12 * e_2 * log((cost_dimension+2)/e_2) / log(cost_dimension)
        self._initial_phase_size = int(ceil(self.delta * total_time))
        self.mwu = MwuMax(self.cost_dimension, self.e)

    def _init_e(self, e: Union[float, None]) -> float:
        if e is None:
            return sqrt(log(self.cost_dimension, 2)/self.capacity)
        else:
            assert e < 0.5
            assert e > 0
            return float(e)

    @property
    def cost_dimension(self):
        return self.p.cost_dimension

    def print_params(self):
        """Print algorithm parameters.
        """
        print(f"capacity = {self.p.capacity}")
        print(f"cost dimension = {self.cost_dimension}")
        print(f"e = {self.e}")
        print(f"estimated z = {self.z}")
        print(f"delta = {self.delta}")
        print(f"initial phase size = {self._initial_phase_size}")
        print(f"total time = {self.total_time}")

    def _compute_z(self) -> float:
        """Compute Z, by solving a scaled offline problem described in the paper's apendix.

        Returns
        -------
        float
            Z parameter
        """
        scaled_cap = (self.delta * self.p.capacity +
                      sqrt(3 * self.delta * self.p.capacity *
                           log((self.cost_dimension+2)/(self.e * self.e))))
        s = self._solver_cls(self.p.get_available_values(), self.p.get_available_costs(), scaled_cap)
        s.solve()
        return 2 * s.optimum_value / (self.delta * self.p.capacity)

    def _choose_index_to_pack(self, current_items: List[Item]) -> int:
        """Given available items for an instant, chooses which item to pack.

        Parameters
        ----------
        current_items : list of float
            List of the items available on the current instant.

        Returns
        -------
        int
            Index of the item with the highest evaluated value.
        """
        if self.current_time < self._initial_phase_size:
            return random.randint(-1, len(current_items)-1)
        else:
            if self.z is None:
                self.z = self._compute_z()
            evaluated_options = [item.reward
                                 - self.z * helper.dot_product(self.mwu.get_probs(), item.costs)
                                 for item in current_items]
            # item that has the highest evaluated value from evaluated_options
            max_idx, max_value = max(enumerate(evaluated_options), key=itemgetter(1))
            # evaluate if its worth to get the item or not
            return max_idx if max_value > 0 else -1

    def _compute_mwu_gains(self, cost: float) -> float:
        """Compute MWU cost(gains) function for a single dimension.

        Parameters
        ----------
        cost : float
            Cost of a single dimension of the cost vector.

        Returns
        -------
        float
            Gains of a single dimension
        """
        return cost - self.p.capacity/self.total_time

    def pack_one(self, available_values: List[float], available_costs: List[List[float]]) -> int:
        """Receives the new instant's items and chooses one to pack.

        Parameters
        ----------
        available_values : list of float
            Value of the items available on the current instant.
        available_costs : list of list of float
            Cost vectors of the items available on the current instant.

        Returns
        -------
        int
            Index of the chosen item or -1 if none of the items were packed.
        """
        current_items = [Item(r, c) for r, c in zip(available_values, available_costs)]
        self.p.set_current_inputs(current_items)
        chosen_idx = self._choose_index_to_pack(current_items)
        if not self.p.item_fits(chosen_idx):
            chosen_idx = -1
        self.p.pack(chosen_idx)
        received_costs = current_items[chosen_idx].costs if chosen_idx != -1 else [0]*self.cost_dimension
        mwu_gains = list(map(self._compute_mwu_gains, received_costs))
        self.mwu.update_weights(mwu_gains)
        self.current_time += 1
        return chosen_idx

    def get_premises_min(self) -> float:
        """Get the minimum value of capacity and `optimum_value` for the
        premises to be valid.

        Returns
        -------
        float
            Minimum value of capacity and `optimum_value` for premises to be valid.
        """
        return log(self.p.cost_dimension) / (self.e*self.e)

    def respect_premises(self) -> bool:
        """Informs if both the algorithm premises (`optimum_value` and capacity) were fulfilled.

        Returns
        -------
        bool
            True if both premises were fulfilled, False otherwise.
        """
        if min(self.optimum_value, self.p.capacity) + 1e-6 < self.get_premises_min():
            return False
        else:
            return True
