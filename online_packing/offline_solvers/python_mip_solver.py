from typing import Any
from mip import Model, MAXIMIZE, CBC, BINARY, OptimizationStatus, xsum, maximize
from online_packing.packing_problem import PackingProblem
from online_packing.offline_solvers.base_solver import BaseSolver


class PythonMIPSolver(BaseSolver):
    solver: Any
    max_seconds: int
    status: int

    def __init__(self, p: PackingProblem, max_seconds: int = 30):
        super().__init__(p)
        self.max_seconds = max_seconds
        self.build_model()

    def build_model(self) -> None:
        self.solver = Model(sense=MAXIMIZE, solver_name=CBC)
        p = self.problem
        m = self.solver
        m.verbose = 0
        x = [[m.add_var(var_type=BINARY)
              for _ in range(p.options_per_instant)]
             for _ in range(p.instants)]
        for dim in range(p.cost_dimension):
            m += xsum(p.available_costs[i][item][dim]*x[i][item]
                      for item in range(p.options_per_instant)
                      for i in range(p.instants)) <= p.capacity  # type: ignore
        for t in range(p.instants):
            m += xsum(x[t][i] for i in range(p.options_per_instant)) == 1
        m.objective = maximize(xsum(p.available_values[i][item]*x[i][item]
                                    for item in range(p.options_per_instant)
                                    for i in range(p.instants)))

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
