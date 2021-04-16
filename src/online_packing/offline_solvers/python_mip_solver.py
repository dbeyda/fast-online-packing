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
        self._build_model()

    def _build_model(self) -> None:
        self.solver = Model(sense=MAXIMIZE, solver_name=CBC)
        m = self.solver
        m.verbose = 0
        x = [[m.add_var(name=f"x[{t}][{opt}]", var_type=BINARY)
              for opt in range(self._options_per_instant)]
             for t in range(self._size)]
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
        if self.status in [OptimizationStatus.OPTIMAL, OptimizationStatus.FEASIBLE]:
            self.optimum_value = self.solver.objective_value
            for idx, v in enumerate(self.solver.vars):
                if abs(v.x) > 1e-6:  # chosen options for an instant are the positive variables
                    chosen_idx = idx % self._options_per_instant
                    self.packed_items.append(chosen_idx)
            for t, packed_idx in enumerate(self.packed_items):
                for dim in range(self._cost_dimension):
                    self.packed_weight_sum[dim] += self._costs[t][packed_idx][dim]
        else:
            self.optimum_value = float("inf")
