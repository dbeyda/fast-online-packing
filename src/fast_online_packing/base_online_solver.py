from abc import ABC, abstractmethod
from typing import List, Type
from fast_online_packing.offline_solvers.base_solver import BaseSolver
from fast_online_packing.offline_solvers.python_mip_solver import PythonMIPSolver
from fast_online_packing.packing_problem import PackingProblem


class BaseOnlineSolver(ABC):
    """Abstract class unifying methods for the online solvers.
    """
    p: PackingProblem
    e: float
    total_time: int
    current_time: int
    optimum_value: float

    def __init__(self, cost_dimension: int, total_time: int, capacity: float, e: float,
                 solver_cls: Type[BaseSolver] = PythonMIPSolver):
        self.p = PackingProblem(capacity, cost_dimension)
        self.current_time = 0
        self.total_time = total_time
        self.optimum_value = float("inf")
        self._solver_cls = solver_cls
        self.e = e

    @property
    def cost_dimension(self):
        return self.p.cost_dimension

    @property
    def capacity(self):
        return self.p.capacity

    @abstractmethod
    def print_params(self) -> None:
        pass

    # this function should also update `current_time`
    @abstractmethod
    def pack_one(self, available_values: List[float], available_costs: List[List[float]]) -> int:
        pass

    # TODO: move this to the Problem class
    def compute_optimum(self) -> float:
        """Solve the problem offline to find out the optimum solution.

        Returns
        -------
        The optimum solution for the problem.
        """
        s = self._solver_cls(self.p.get_available_values(),
                             self.p.get_available_costs(), self.p.capacity)
        s.solve()
        self.optimum_value = s.optimum_value
        return s.optimum_value

    def print_result(self) -> None:
        """Print usefull information about the algorithm execution.
        """
        print(f"- Opt: {self.optimum_value}")
        print(f"- Alg: {self.p.packed_rewards_sum}")
        print(f"- % Alg = {self.p.packed_rewards_sum/self.optimum_value :.3f} * Opt")
