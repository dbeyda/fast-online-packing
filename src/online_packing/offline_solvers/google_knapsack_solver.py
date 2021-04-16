from ortools.algorithms import pywrapknapsack_solver
from typing import List, Any, Tuple, Union
from online_packing.offline_solvers.base_solver import BaseSolver


class GoogleKnapsackSolver(BaseSolver):
    solver: Any
    adapted_values: List[int]
    adapted_costs: List[List[int]]
    adapted_capacity: List[int]
    decimal_places: int

    def __init__(self, values: List[List[Union[float, int]]],
                 costs: List[List[List[Union[float, int]]]],
                 capacity: float,
                 decimal_places: int = 6):
        GoogleKnapsackSolver.validate_instance(values, costs)
        super().__init__(values, costs, capacity)
        self.decimal_places = decimal_places
        self.adapted_values, self.adapted_costs, self.adapted_capacity = self._adapter()
        self.solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver
                                                           .KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
                                                           'KnapsackExample')
        self.solver.Init(self.adapted_values, self.adapted_costs, self.adapted_capacity)

    @staticmethod
    def validate_instance(values: List[List[Union[float, int]]],
                          costs: List[List[List[Union[float, int]]]]):
        for value_options in values:
            if(len(value_options) != 2):
                raise Exception("Each day should have two value options: a real one, and a 0 one.")
        for cost_options in costs:
            if(len(cost_options) != 2):
                raise Exception("Each day should have two cost options: a real one, and a 0 one.")

    def _adapter(self) -> Tuple[List[int], List[List[int]], List[int]]:
        factor = pow(10, self.decimal_places)
        capacity = [int(self._capacity * factor)] * self._cost_dimension
        values = [int(t[0]*factor) for t in self._values]
        costs = [[int(self._costs[t][0][dim]*factor)
                  for t in range(self._size)]
                 for dim in range(self._cost_dimension)]
        return values, costs, capacity

    def solve(self):
        factor = pow(10, self.decimal_places)
        self.optimum_value: float = self.solver.Solve() / factor
        self.packed_items = list()

        for i in range(len(self.adapted_values)):
            # if item was packed it was first option of the instant
            # if item was not packed, second option is packing nothing
            packed_idx = 0 if self.solver.BestSolutionContains(i) else 1
            self.packed_items.append(packed_idx)
            for dim in range(self._cost_dimension):
                self.packed_weight_sum[dim] += self._costs[i][packed_idx][dim]
