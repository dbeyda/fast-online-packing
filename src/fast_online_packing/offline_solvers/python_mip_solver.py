from typing import Any, Union, List
from mip import Model, MAXIMIZE, CBC, BINARY, OptimizationStatus, xsum, maximize
from fast_online_packing.offline_solvers.base_solver import BaseSolver


class PythonMIPSolver(BaseSolver):
    """Python-MIP Solver, used to model and solve the offline Packing LP Problem,
    using a COIN-OR Branch and Cut (CBC) solver.

    Parameters
    ----------
    values
        Refer to the BaseSolver parameters.
    costs
        Refer to the BaseSolver parameters.
    capacity
        Refer to the BaseSolver parameters.
    max_seconds : int, default=30
        Maximum time spent searching for better solutions, in seconds.

    Attributes
    ----------
    optimum_value : float or int
        The optimum value found for the LP problem.
    packed_items : list of int
        A list containing the indexes of the items chosen in each instant.
    packed_weight_sum : list of float
        A list containing the optimal solution's total cost for each dimension.
    solver
        The instance of the Python-MIP solver.
    max_seconds : int
        Maximum time spent searching for better solutions, in seconds.
    status : {mip.OptimizationStatus.OPTIMAL, mip.OptimizationStatus.FEASIBLE, \
              mip.OptimizationStatus.INFEASIBLE}
        Result of the optimization procedure.

    Methods
    -------
    solve()
        Solves the LP problem.
    print_result()
        Inherited from BaseSolver.

    Notes
    -----
    This is a Mixed Integer Programming modeler and solver, being much more flexible than
    the Google Knapsack Solver, accepting all types of variantions of the problem: more than one
    item per instant, obligatory packing or flexible packing.

    Read more about the `Python-MIP Solver`_.

    .. _Python-MIP Solver: https://docs.python-mip.com/en/latest/index.html
    """
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
        """Initializes the Python-MIP solver and builds a model for the Linear Programming
        problem, setting an objective function and constraints.

        Returns
        -------
        None
        """
        self.solver = Model(sense=MAXIMIZE, solver_name=CBC)
        m = self.solver
        m.verbose = 0
        # creating variables for all instants and options
        x = [[m.add_var(name=f"x[{t}][{opt}]", var_type=BINARY)
              for opt in range(self._options_per_instant)]
             for t in range(self._size)]
        # setting capacity constraint
        for dim in range(self._cost_dimension):
            m += xsum(self._costs[i][item][dim]*x[i][item]
                      for item in range(self._options_per_instant)
                      for i in range(self._size)) <= self._capacity  # type: ignore
        # setting constraint to only choose one item per instant
        for t in range(self._size):
            m += xsum(x[t][i] for i in range(self._options_per_instant)) <= 1  # type: ignore
        # setting objective function
        m.objective = maximize(xsum(self._values[i][item]*x[i][item]
                                    for item in range(self._options_per_instant)
                                    for i in range(self._size)))

    def solve(self):
        """Solves the optimization problem and sets `status`, `optimum_value`,
        `packed_items` and `packed_weight_sum`.

        Returns
        -------
        None
        """
        self.packed_items = [-1] * self._size
        self.status = self.solver.optimize(max_seconds=self.max_seconds)
        if self.status in [OptimizationStatus.OPTIMAL, OptimizationStatus.FEASIBLE]:
            self.optimum_value = self.solver.objective_value
            for idx, v in enumerate(self.solver.vars):
                if abs(v.x) > 1e-6:  # chosen options for an instant are the positive variables
                    chosen_idx = idx % self._options_per_instant
                    time_instant = idx // self._options_per_instant
                    self.packed_items[time_instant] = chosen_idx
            for t, packed_idx in enumerate(self.packed_items):
                if t >= 0:
                    for dim in range(self._cost_dimension):
                        self.packed_weight_sum[dim] += self._costs[t][packed_idx][dim]
        else:
            self.optimum_value = float("inf")
