from typing import List
from random import random
from online_packing.packing_problem import PackingProblem
from copy import deepcopy


def new_packing_problem(n_instants: int, cost_dim: int, itens_per_instant: int = 1,
                        mandatory_packing: bool = True) -> PackingProblem:
    # setting mandatory_packing=False adds a new item in each instant
    # have value=0 and cost=0 in all dimensions
    cap = random() * n_instants/4

    values: List[List[float]] = [[random() for _ in range(itens_per_instant)] for _ in range(n_instants)]
    if not mandatory_packing:
        for t in values:
            t.append(0.0)

    weights: List[List[List[float]]] = [[] for _ in range(n_instants)]

    for t in weights:
        for _ in range(itens_per_instant):
            t.append([random() for _ in range(cost_dim)])
        if not mandatory_packing:
            t.append([0.0 for _ in range(cost_dim)])

    return PackingProblem(values.copy(), deepcopy(weights), cap, mandatory_packing)
