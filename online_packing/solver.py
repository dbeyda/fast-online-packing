from abc import ABC, abstractmethod
from ortools.algorithms import pywrapknapsack_solver
from typing import List, Any
from online_packing.packing_problem import PackingProblem


class AbstractPackingSolver(ABC):
    problem: PackingProblem

    def __init__(self, p: PackingProblem):
        self.problem = p

    @abstractmethod
    def solve(self) -> None:
        pass


class GooglePackingSolver(AbstractPackingSolver):
    solver: Any
    values: List[int]
    costs: List[List[int]]
    capacity: List[int]
    decimal_places: int

    def __init__(self, p: PackingProblem, decimal_places: int = 6):
        super().__init__(p)
        self.decimal_places = decimal_places
        self.integer_adapter(self.problem)
        self.solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver
                                                           .KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
                                                           'KnapsackExample')
        self.solver.Init(self.values, self.costs, self.capacity)

    def solve(self):
        result: int = self.solver.Solve()
        self.packed_value: float = result / pow(10, self.decimal_places)

    def integer_adapter(self, p: PackingProblem) -> None:
        factor = pow(10, self.decimal_places)
        self.values = list(map(lambda x: int(factor * x), p.values))
        self.costs = [list(map(lambda x: int(factor * x), dimension_costs))
                      for dimension_costs in p.costs]
        self.capacity = [int(p.capacity * factor)] * p.cost_dimension

    def print_result(self):
        print('Total value =', self.packed_value)
        packed_items = []
        packed_weights = []
        total_weight = [0] * self.problem.cost_dimension

        for i in range(len(self.values)):
            if self.solver.BestSolutionContains(i):
                packed_items.append(i)
                packed_weights.append(self.costs[0][i])
                for dim in range(self.problem.cost_dimension):
                    total_weight[dim] += self.costs[dim][i]
        for dim in range(self.problem.cost_dimension):
            print(f"\tTotal weight dim {dim}: {total_weight[dim]} / {self.capacity[0]}")
        print('Packed items:', packed_items)
        print('Packed_weights:', packed_weights)


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
