from typing import Any, Union, List
from mip import Model, MAXIMIZE, CBC, BINARY, OptimizationStatus, xsum, maximize
from online_packing.offline_solvers.base_solver import BaseSolver


class PythonMIPSolver(BaseSolver):
    solver: Any
    max_seconds: int
    status: int

    def __init__(self, values: List[List[Union[float, int]]],
                 costs: List[List[List[Union[float, int]]]],
                 capacity: Union[float, int],
                 max_seconds: int = 30):
        super().__init__(values, costs, capacity)
        self.max_seconds = max_seconds
        self.build_model()

    def build_model(self) -> None:
        self.solver = Model(sense=MAXIMIZE, solver_name=CBC)
        m = self.solver
        m.verbose = 0
        x = [[m.add_var(var_type=BINARY)
              for _ in range(self._options_per_instant)]
             for _ in range(self._size)]
        for dim in range(self._cost_dimension):
            m += xsum(self._costs[i][item][dim]*x[i][item]
                      for item in range(self._options_per_instant)
                      for i in range(self._size)) <= self._capacity  # type: ignore
        for t in range(self._size):
            m += xsum(x[t][i] for i in range(self._options_per_instant)) == 1
        m.objective = maximize(xsum(self._values[i][item]*x[i][item]
                                    for item in range(self._options_per_instant)
                                    for i in range(self._size)))

    def solve(self):
        self.status = self.solver.optimize(max_seconds=self.max_seconds)

    def print_result(self):
        m = self.solver
        if self.status == OptimizationStatus.OPTIMAL:
            print(f"optimal solution cost {m.objective_value:.5f} found")
        elif self.status == OptimizationStatus.FEASIBLE:
            print(f"sol.cost {m.objective_value:.5f} found, best possible: {m.objective_bound:.5f}")
        elif self.status == OptimizationStatus.NO_SOLUTION_FOUND:
            print("no feasible solution found, lower bound is: {m.objective_bound:.5f}")
