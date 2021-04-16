from math import log, sqrt
from typing import List, Union
import random
from online_packing.mwu_max import MwuMax
from enum import Enum, auto
from operator import itemgetter
from online_packing import helper
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.packing_problem import PackingProblem


class OnlineSolver:
    class State(Enum):
        RUNNING = auto()
        FINISHED = auto()

    p: PackingProblem
    e: float
    cost_dimension: int
    theta: MwuMax
    z: Union[float, None] = None
    delta: float
    total_time: int
    current_time: int
    state: State

    # TODO: receive different solvers in this function
    def __init__(self, e: float, cost_dimension: int, total_time: int, capacity: float):
        self.p = PackingProblem(capacity, cost_dimension)
        self._init_params(e, cost_dimension, total_time)
        self._solver_cls = PythonMIPSolver
        self.state = OnlineSolver.State.RUNNING

    def _init_params(self, e: float, cost_dimension: int, total_time: int):
        # TODO test if e is in the valid range
        self.e = e
        self.z = None
        # TODO set delta using e
        e_2 = self.e * self.e
        self.delta = 12 * e_2 * log((cost_dimension+2)/e_2) / log(cost_dimension)
        # self.delta = 0.2
        self.current_time = 1
        self._initial_phase_size = self.delta * total_time
        self.total_time = total_time
        self.cost_dimension = cost_dimension
        self.theta = MwuMax(self.cost_dimension, self.e)

    def print_params(self):
        print("cost_dimension = ", self.cost_dimension)
        print("e = ", self.e)
        print("delta = ", self.delta)
        print("_initial_phase_size = ", self._initial_phase_size)
        print("total_time = ", self.total_time)

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
            # return len(available_values)-1
            return random.randint(0, len(available_values)-1)
        else:
            if self.z is None:
                self.z = self._compute_z()
                print(f"z set to {self.z}")
            evaluated_options = [available_values[i]
                                 - self.z * helper.dot_product(self.theta.get_probs(), available_costs[i])
                                 for i in range(len(available_values))]
            return max(enumerate(evaluated_options), key=itemgetter(1))[0]

    def _compute_mwu_gains(self, x: float) -> float:
        return x - self.p.get_capacity()/self.total_time

    def pack_one(self, available_values: List[float], available_costs: List[List[float]]):
        self.p.set_current_inputs(available_values, available_costs)
        if self.state is OnlineSolver.State.RUNNING:
            chosen_idx = self._choose_index_to_pack(available_values, available_costs)
            if self.p.item_fits(chosen_idx):
                self.p.pack(chosen_idx)
                mwu_gains = list(map(self._compute_mwu_gains, available_costs[chosen_idx]))
                self.theta.update_weights(mwu_gains)
            else:
                self.p.end_packing()
                self.state = OnlineSolver.State.FINISHED
        self.current_time += 1

    def compute_optimum(self) -> float:
        s = self._solver_cls(self.p.get_available_values(),
                             self.p.get_available_costs(), self.p.get_capacity())
        s.solve()
        return s.optimum_value
