from math import log, sqrt, ceil
from typing import List, Union, Type
import random
from online_packing.mwu_max import MwuMax
from operator import itemgetter
from online_packing import helper
from online_packing.offline_solvers.base_solver import BaseSolver
from online_packing.packing_problem import PackingProblem


class OnlineSolver:
    p: PackingProblem
    e: float
    theta: MwuMax
    z: Union[float, None]
    delta: float
    total_time: int
    current_time: int
    optimum_value: float

    # TODO: receive different solvers in this function
    def __init__(self, e: float, cost_dimension: int, total_time: int, capacity: float,
                 solver_cls: Type[BaseSolver]):
        self.z = None
        self.p = PackingProblem(capacity, cost_dimension)
        self._init_params(e, cost_dimension, total_time, capacity)
        self._solver_cls = solver_cls
        self.optimum_value = float("inf")

    def _init_params(self, e: float, cost_dimension: int, total_time: int, capacity: float):
        # TODO test if e is in the valid range
        # self.e = sqrt(log(cost_dimension, 2)/capacity)
        # if (e < self.e-1e-6):
        #     raise Exception(f"Param e = {e} not valid. For cap = {capacity}, e >= {self.e}")
        self.e = e
        self.z = None
        e_2 = self.e * self.e
        self.delta = 12 * e_2 * log((cost_dimension+2)/e_2) / log(cost_dimension)
        self.current_time = 1
        self._initial_phase_size = int(ceil(self.delta * total_time))
        self.total_time = total_time
        self.theta = MwuMax(self.cost_dimension, self.e)

    @property
    def cost_dimension(self):
        return self.p.get_cost_dimension()

    def print_params(self):
        print(f"\tcapacity = {self.p.get_capacity()}")
        print(f"\tcost dimension = {self.cost_dimension}")
        print(f"\te = {self.e}")
        print(f"\tdelta = {self.delta}")
        print(f"\tinitial phase size = {self._initial_phase_size}")
        print(f"\ttotal time = {self.total_time}")

    def _compute_z(self) -> float:
        scaled_cap = (self.delta * self.p.get_capacity() +
                      sqrt(3 * self.delta * self.p.get_capacity() *
                           log((self.cost_dimension+2)/(self.e * self.e))))
        s = self._solver_cls(self.p.get_available_values(), self.p.get_available_costs(), scaled_cap)
        s.solve()
        return 2 * s.optimum_value / (self.delta * self.p.get_capacity())

    def _choose_index_to_pack(self, available_values: List[float],
                              available_costs: List[List[float]]) -> int:
        if self.current_time <= self._initial_phase_size:
            return random.randint(0, len(available_values)-1)
        else:
            if self.z is None:
                self.z = self._compute_z()
            evaluated_options = [available_values[i]
                                 - self.z * helper.dot_product(self.theta.get_probs(), available_costs[i])
                                 for i in range(len(available_values))]
            return max(enumerate(evaluated_options), key=itemgetter(1))[0]

    def _compute_mwu_gains(self, x: float) -> float:
        return x - self.p.get_capacity()/self.total_time

    def pack_one(self, available_values: List[float], available_costs: List[List[float]]):
        self.p.set_current_inputs(available_values, available_costs)
        if self.p.get_state() is PackingProblem.State.RUNNING:
            chosen_idx = self._choose_index_to_pack(available_values, available_costs)
            if self.p.item_fits(chosen_idx):
                self.p.pack(chosen_idx)
                mwu_gains = list(map(self._compute_mwu_gains, available_costs[chosen_idx]))
                self.theta.update_weights(mwu_gains)
            else:
                self.p.end_packing()
        self.current_time += 1

    def compute_optimum(self) -> float:
        s = self._solver_cls(self.p.get_available_values(),
                             self.p.get_available_costs(), self.p.get_capacity())
        s.solve()
        self.optimum_value = s.optimum_value
        return s.optimum_value

    def print_result(self) -> None:
        pass

    def get_premises_min(self) -> float:
        return log(self.p.get_cost_dimension()) / (self.e*self.e)

    def respect_premises(self) -> bool:
        if min(self.optimum_value, self.p.get_capacity()) + 1e-6 < self.get_premises_min():
            return False
        else:
            return True
