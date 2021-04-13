from typing import List, Union, Any
import random
from operator import itemgetter
from online_packing import helper
from online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from online_packing.packing_problem import PackingProblem


class OnlineSolver:
    p: PackingProblem
    e: float
    theta: List[float]
    z: float
    delta: float
    total_time: int
    current_time: int = 0

    def __init__(self, e: float, total_time: int, capacity: float = 0.0,
                 p: Union[PackingProblem, Any] = None):
        self.p = p if p else PackingProblem(capacity)
        # TODO test if e is in the valid range
        self.e = e
        # TODO set delta using e
        delta = 1-e
        self.total_time = total_time
        self.initial_phase_size = delta * total_time

    def _choose_index_to_pack(self, available_values: List[float], available_costs: List[List[float]]) -> int:
        if self.current_time < self.total_time:
            return random.randint(0, len(available_values)-1)
        else:
            evaluated_options = [available_values[i]
                                 - self.z * helper.dot_product(self.theta, available_costs[i])
                                 for i in range(len(available_values))]
            return max(enumerate(evaluated_options), key=itemgetter(1))[0]

    def pack_one(self, available_values: List[float], available_costs: List[List[float]]) -> int:
        # pick one
        chosen_idx = self._choose_index_to_pack(available_values, available_costs)
        self.p.pack(chosen_idx)
