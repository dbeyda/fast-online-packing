from ortools.algorithms import pywrapknapsack_solver
from typing import List, Any, Tuple, Union
from online_packing.offline_solvers.base_solver import BaseSolver


class GoogleKnapsackSolver(BaseSolver):
    solver: Any
    adapted_values: List[int]
    adapted_costs: List[List[int]]
    adapted_capacity: List[int]
    decimal_places: int
    optimum_value: float

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

    def print_result(self):
        factor = pow(10, self.decimal_places)
        print(f"Total value = {self.optimum_value:.5f}")
        packed_items = []
        packed_weights = []
        total_weight = [0] * self._cost_dimension

        for i in range(len(self.adapted_values)):
            if self.solver.BestSolutionContains(i):
                packed_items.append(i)
                packed_weights.append(self.adapted_costs[0][i] / factor)
                for dim in range(self._cost_dimension):
                    total_weight[dim] += self.adapted_costs[dim][i] / factor
        for dim in range(self._cost_dimension):
            print(
                f"\tTotal weight dim {dim}: \
                    {total_weight[dim]:.5f} / {self.adapted_capacity[dim] / factor:.5f}")
        print(f"Packed items: {packed_items}")
        print(f"Packed_weights: {packed_weights}")


#########################################################
# values = [
#     360.0, 83.0, 59.0, 130.0, 431.0, 67.0, 230.0, 52.0, 93.0, 125.0, 670.0,
#     892.0, 600.0, 38.0, 48.0, 147.0,
#     78.0, 256.0, 63.0, 17.0, 120.0, 164.0, 432.0, 35.0, 92.0, 110.0, 22.0,
#     42.0, 50.0, 323.0, 514.0, 28.0,
#     87.0, 73.0, 78.0, 15.0, 26.0, 78.0, 210.0, 36.0, 85.0, 189.0, 274.0,
#     43.0, 33.0, 10.0, 19.0, 389.0, 276.0,
#     312.0
# ]
# weights = [[
#     7.0, 0.0, 30.0, 22.0, 80.0, 94.0, 11.0, 81.0, 70.0, 64.0, 59.0, 18.0, 0.0,
#     36.0, 3.0, 8.0, 15.0, 42.0, 9.0, 0.0,
#     42.0, 47.0, 52.0, 32.0, 26.0, 48.0, 55.0, 6.0, 29.0, 84.0, 2.0, 4.0, 18.0,
#     56.0, 7.0, 29.0, 93.0, 44.0, 71.0,
#     3.0, 86.0, 66.0, 31.0, 65.0, 0.0, 79.0, 20.0, 65.0, 52.0, 13.0
# ], [
#     1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
#     1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
#     1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
#     1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
#     1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
# ]]
# cap = 850.0
