from ortools.algorithms import pywrapknapsack_solver
from typing import List, Any, Tuple, Union
from fast_online_packing.offline_solvers.base_solver import BaseSolver


class GoogleKnapsackSolver(BaseSolver):
    """Google OR-Tools solver for the multi-dimensional Knapsack
    problem using integer values.

    Parameters
    ----------
    values
        Refer to the BaseSolver parameters.
    costs
        Refer to the BaseSolver parameters.
    capacity
        Refer to the BaseSolver parameters.
    decimal_places : int
        Decimal precision used to scale floats in values and costs into integers.

    Attributes
    ----------
    optimum_value : float or int
        The optimum value found for the LP problem.
    packed_items : list of int
        A list containing the indexes of the items chosen in each instant.
    packed_weight_sum : list of float
        A list containing the optimal solution's total cost for each dimension.
    solver
        The instance of the used OR-Tools `pywrapknapsack_solver.KnapsackSolver` solver.
    adapted_values : list of int
        `values` scaled into an integer using `decimal_places` decimal places as precision.
    adapted_costs : list of list of int
        `costs` scaled into an integer using `decimal_places` decimal places as precision.
    adapted_capacity : list of int
        A list with, for every cost dimension, the same `capacity` scaled into an integer using
        `decimal_places` decimal places as precision.
    decimal_places : int
        Decimal precision used to scale floats in `values` and `costs` into integers.

    Methods
    -------
    solve()
        Solves the LP problem.
    print_result()
        Inherited from BaseSolver.
    validate_instance(values, costs)
        Check if an offline packing LP instance is valid for this solver.

    Notes
    -----
    The google solver used here does not accept floating point numbers, as it considers the
    problem as a discrete one. Thus, we multiply every value, cost and capacity by
    :math:`10^n` where :math:`n` is `decimal_places`.

    Also, this solver only accepts one item options per instant.

    *Validity Conditions:*
    Also, there are variantions of the packing problem. Some allow the algorithm
    to do nothing, not packing any item, in an instant. Some compel the algorithm
    to make a choice in every instant. The google solver only accepts instances
    where it is not required to pack an item in every instant. This solver also only
    accepts instances where there is only one item available per instant.

    Read more about the `Google OR-Tools Knapsack Solver`_.

    .. _Google OR-Tools Knapsack Solver: https://developers.google.com/optimization/bin/knapsack
    """
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
                          costs: List[List[List[Union[float, int]]]]) -> None:
        """Check if a given instance is valid for this solver. Refer to the
        *Notes* to check validity conditions.

        Parameters
        ----------
        values
            Values for the instance. For format, refer to BaseSolver parameters.
        costs
            Costs for the instance. For format, refer to BaseSolver parameters.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If problem instance is not valid.
        """
        for value_options, cost_options in zip(values, costs):
            if(len(value_options) > 1 or len(cost_options) > 1):
                raise Exception("GoogleKnapspackSolver only works with one item per instant.")

    def _adapter(self) -> Tuple[List[int], List[List[int]], List[int]]:
        """Adapts instance values from floats into integers.

        Returns
        -------
        values : list of int
            List containing the adapted values of each instant (only one item per instant in this solver).
        costs : list of list of int
            List containing, for each instant, the item's adapted costs.
        capacity : list of int
            List containing adapted capacity, the same for each dimension.

        """
        factor = pow(10, self.decimal_places)
        capacity = [int(self._capacity * factor)] * self._cost_dimension
        values = [int(t[0]*factor) for t in self._values]
        costs = [[int(self._costs[t][0][dim]*factor)
                  for t in range(self._size)]
                 for dim in range(self._cost_dimension)]
        return values, costs, capacity

    def solve(self):
        """Try to solve the LP problem and sets `optimum_value`, `packed_items`
        and `packed_weight_sum`.

        Returns
        -------
        None
        """
        factor = pow(10, self.decimal_places)
        self.optimum_value: float = self.solver.Solve() / factor
        self.packed_items = [-1] * self._size

        for i in range(len(self.adapted_values)):
            # if item was packed it was first option of the instant, meaning index 0
            if self.solver.BestSolutionContains(i):
                self.packed_items[i] = 0
                for dim in range(self._cost_dimension):
                    self.packed_weight_sum[dim] += self._costs[i][0][dim]
