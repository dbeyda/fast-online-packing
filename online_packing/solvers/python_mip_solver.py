from typing import Any
from mip import Model, MAXIMIZE, CBC, BINARY, OptimizationStatus, xsum, maximize
from online_packing.packing_problem import PackingProblem
from online_packing.solvers.base_solver import BaseSolver


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
            m += xsum(p.costs[i][item][dim]*x[i][item]
                      for item in range(p.options_per_instant)
                      for i in range(p.instants)) <= p.capacity  # type: ignore
        for t in range(p.instants):
            m += xsum(x[t][i] for i in range(p.options_per_instant)) == 1
        m.objective = maximize(xsum(p.values[i][item]*x[i][item]
                                    for item in range(p.options_per_instant)
                                    for i in range(p.instants)))

    def solve(self):
        self.status = self.solver.optimize(max_seconds=self.max_seconds)

    def print_result(self):
        m = self.solver
        if self.status == OptimizationStatus.OPTIMAL:
            print('optimal solution cost {} found'.format(m.objective_value))
        elif self.status == OptimizationStatus.FEASIBLE:
            print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
        elif self.status == OptimizationStatus.NO_SOLUTION_FOUND:
            print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
        if self.status == OptimizationStatus.OPTIMAL \
                or self.status == OptimizationStatus.FEASIBLE:
            print('solution:')
            for v in m.vars:
                if abs(v.x) > 1e-6:  # only printing non-zeros
                    print('{} : {}'.format(v.name, v.x))
