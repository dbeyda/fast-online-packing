from typing import List, Any
from random import random
from online_packing.packing_problem import PackingProblem
from copy import deepcopy


def new_packing_problem(t: int, cost_dim: int) -> PackingProblem:
    values = []
    weights: List[List[Any]] = [[] for _ in range(cost_dim)]
    cap = random() * t/4

    for _ in range(t):
        values.append(random())

    for dim in range(cost_dim):
        for _ in range(t):
            weights[dim].append(random())

    return PackingProblem(values.copy(), deepcopy(weights), cap)
