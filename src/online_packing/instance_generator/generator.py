"""This module helps with generation of instances for our problem
"""
from typing import List, Tuple
from random import random
from copy import deepcopy
from math import log, sqrt


def generate_valid_instance(n_instants: int, cost_dim: int, items_per_instant: int = 1,
                            mandatory_packing: bool = True) -> \
        Tuple[List[List[float]], List[List[List[float]]], float, float]:
    """blablab
    """
    # setting mandatory_packing=False adds a new item in each instant
    # have value=0 and cost=0 in all dimensions
    assert items_per_instant > 0
    assert cost_dim > 0

    values: List[List[float]] = [[random() for _ in range(items_per_instant)] for _ in range(n_instants)]
    if not mandatory_packing:
        for t in values:
            t.append(0.0)

    weights: List[List[List[float]]] = [[] for _ in range(n_instants)]

    for t in weights:
        for _ in range(items_per_instant):
            t.append([random() for _ in range(cost_dim)])
        if not mandatory_packing:
            t.append([0.0 for _ in range(cost_dim)])

    # sort cap until delta < 1
    cap = get_new_cap(n_instants)
    e = sqrt(log(cost_dim, 2)/cap)
    e_2 = e*e
    delta = 12 * e_2 * log((cost_dim+2)/e_2) / log(cost_dim)
    while (delta > 0.6 or e > 0.5-1e-6):
        cap = get_new_cap(n_instants)
        e = sqrt(log(cost_dim, 2)/cap)
        e_2 = e*e
        delta = 12 * e_2 * log((cost_dim+2)/e_2) / log(cost_dim)
        print(f"delta={delta}")

    return values.copy(), deepcopy(weights), cap, e


def get_new_cap(n_instants: float) -> float:
    return random() * n_instants/2
