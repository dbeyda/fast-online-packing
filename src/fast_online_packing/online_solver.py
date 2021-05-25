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
from fast_online_packing.packing_problem import PackingProblem


class OnlineSolver:
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
        Count of the instant the algorithm currently is. 1-indexed.
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

    p: PackingProblem
    e: float
    mwu: MwuMax
    z: Union[float, None]
    delta: float
    total_time: int
    current_time: int
    optimum_value: float

    # TODO: receive different solvers in this function
    def __init__(self, cost_dimension: int, total_time: int, capacity: float, e: Union[float, None] = None,
                 solver_cls: Type[BaseSolver] = PythonMIPSolver):
        self.z = None
        self.p = PackingProblem(capacity, cost_dimension)
        self._init_params(cost_dimension, total_time, capacity, e)
        self._solver_cls = solver_cls
        self.optimum_value = float("inf")

    def _init_params(self, cost_dimension: int, total_time: int, capacity: float,
                     e: Union[float, None]) -> None:
        """Initializes method parameters
        """
        if e is None:
            self.e = sqrt(log(cost_dimension, 2)/capacity)
        else:
            assert e + 1e-6 < 0.5
            assert e - 1e-6 > 0
            self.e = e
        self.z = None
        e_2 = self.e * self.e
        self.delta = 12 * e_2 * log((cost_dimension+2)/e_2) / log(cost_dimension)
        self.current_time = 1
        self._initial_phase_size = int(ceil(self.delta * total_time))
        self.total_time = total_time
        self.mwu = MwuMax(self.cost_dimension, self.e)

    @property
    def cost_dimension(self):
        return self.p.get_cost_dimension()

    def print_params(self):
        """Print algorithm parameters.
        """
        print(f"capacity = {self.p.get_capacity()}")
        print(f"cost dimension = {self.cost_dimension}")
        print(f"e = {self.e}")
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
        scaled_cap = (self.delta * self.p.get_capacity() +
                      sqrt(3 * self.delta * self.p.get_capacity() *
                           log((self.cost_dimension+2)/(self.e * self.e))))
        s = self._solver_cls(self.p.get_available_values(), self.p.get_available_costs(), scaled_cap)
        s.solve()
        return 2 * s.optimum_value / (self.delta * self.p.get_capacity())

    def _choose_index_to_pack(self, available_values: List[float],
                              available_costs: List[List[float]]) -> int:
        """Given available items for an instant, chooses which item to pack.

        Parameters
        ----------
        available_values : list of float
            Value of the items available on the current instant.
        available_costs : list of list of float
            Cost vectors of the items available on the current instant.

        Returns
        -------
        int
            Index of the item with the highest evaluated value.
        """
        if self.current_time <= self._initial_phase_size:
            return random.randint(-1, len(available_values)-1)
        else:
            if self.z is None:
                self.z = self._compute_z()
            evaluated_options = [available_values[i]
                                 - self.z * helper.dot_product(self.mwu.get_probs(), available_costs[i])
                                 for i in range(len(available_values))]
            # item that has the highest evaluated value from evaluated_options
            max_idx, max_value = max(enumerate(evaluated_options), key=itemgetter(1))
            # evaluate if its worth to get the item or not
            return max_idx if max_value > 0+1e-6 else -1

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
        return cost - self.p.get_capacity()/self.total_time

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
        self.p.set_current_inputs(available_values, available_costs)
        chosen_idx = self._choose_index_to_pack(available_values, available_costs)
        if not self.p.item_fits(chosen_idx):
            chosen_idx = -1
        self.p.pack(chosen_idx)
        received_costs = available_costs[chosen_idx] if chosen_idx != -1 else [0]*self.cost_dimension
        mwu_gains = list(map(self._compute_mwu_gains, received_costs))
        self.mwu.update_weights(mwu_gains)
        self.current_time += 1
        return chosen_idx

    def compute_optimum(self) -> float:
        """Solve the problem offline to find out the optimum solution.

        Returns
        -------
        The optimum solution for the problem.
        """
        s = self._solver_cls(self.p.get_available_values(),
                             self.p.get_available_costs(), self.p.get_capacity())
        s.solve()
        self.optimum_value = s.optimum_value
        return s.optimum_value

    def print_result(self) -> None:
        """Print usefull information about the algorithm execution.
        """
        print(f"Opt: {self.optimum_value}")
        print(f"Alg: {self.p._packed_value_sum}")  # type: ignore
        print(f"Score Alg = {self.p._packed_value_sum/self.optimum_value :.3f} * Opt")  # type: ignore
        print(f"     min {{B, TOPT}} = {self.get_premises_min():.3f}")
        print(f"     B = {self.p.get_capacity()}")
        print(f"     TOPT = {self.optimum_value}")

    def get_premises_min(self) -> float:
        """Get the minimum value of capacity and `optimum_value` for the
        premises to be valid.

        Returns
        -------
        float
            Minimum value of capacity and `optimum_value` for premises to be valid.
        """
        return log(self.p.get_cost_dimension()) / (self.e*self.e)

    def respect_premises(self) -> bool:
        """Informs if both the algorithm premises (`optimum_value` and capacity) were fulfilled.

        Returns
        -------
        bool
            True if both premises were fulfilled, False otherwise.
        """
        if min(self.optimum_value, self.p.get_capacity()) + 1e-6 < self.get_premises_min():
            return False
        else:
            return True
