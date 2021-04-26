"""This module helps with generation of instances for our problem.
"""
from typing import List, Tuple, Callable
import random
from copy import deepcopy
from math import log, sqrt, floor


def _find_cap(target_delta: float, cost_dim: int) -> float:
    """Find capacity such that epsilon <= 0.5 (MWU guarantees) and
    delta < target_delta (so we dont waste many values estimating Z).

    Here we consider only integer values for the capacity, and
    use binary search to find the smallest valid capacity in
    logarithmic time.
    """
    # function to compute the best (lowest) epsilon
    e: Callable[[float], float] = lambda c: sqrt(log(cost_dim, 2)/c)
    # function to compute hardest/"most restrictive" (lowest) delta based on capacity
    delta: Callable[[float], float] = lambda c: (12 / c) * log((cost_dim+2)*c / log(cost_dim))

    # Binary search to find ideal capacity
    left: float = 12 * log((cost_dim+2)/log(cost_dim))
    right: float = 1e10
    while left < right:
        mid: float = floor((left + right) / 2)
        if (delta(mid) > target_delta or e(mid) > 0.5-1e-6):
            left = mid+1
        else:
            right = mid
    return left


def generate_valid_instance(target_delta: float, n_instants: int, cost_dim: int, items_per_instant: int = 1,
                            mandatory_packing: bool = True) -> \
        Tuple[List[List[float]], List[List[List[float]]], float, float]:
    """Generates values for a problem instance that respect guarantees premises,
    thus, theoric guarantees should be valid (see Notes section below).

    Parameters
    ----------
    target_delta : float
        Capacity will be set with the constraint that delta <= `target_delta`.
    n_instants : int
        Number of instants to be generated.
    cost_dim : int
        Dimension of the cost vectors to be generated.
    items_per_instant : int
        Number of items that should be available in each instant.
    mandatory_packing : bool
        If instance should enforce the need to always pack an item in every instant.

    Returns
    -------
    values : list of list of float
        A list containing, for each instant, a list with that instant item's values.
    costs : list of list of list of float
        A list containing, for each instant, a list with that instant item's cost vectors.
    cap : float
        A random problem capacity.
    e : float
        The best theorical epsilon for the generated problem.

    Notes
    -----
    Setting ``mandatory_packing=False`` will cause this function to add, for each instant,
    an extra item with :math:`value = 0` and :math:`cost = 0` for every dimension, allowing
    the player to pack that item when he wants to "do nothing" in some instant.

    `target_delta` should be calibrated relative to `n_instants`. Setting a `target_delta`
    too low can cause the :math:`optimum\\_value\\_sum \\geq \\log d / \\epsilon^2` premise to be violated.
    Setting `target_delta` too high is not ideal since the algorithm chooses the items randomly in the first
    `target_delta` fraction of instants.

    The only premise that is guaranteed here is that :math:`cap \\geq \\log d / \\epsilon^2`. The
    :math:`optimum\\_value\\_sum \\geq \\log d / \\epsilon^2` premise is not asserted since it would
    require solving the instance to find `optimum_value_sum`, making this function slow. Setting
    a higher `target_delta` will increase the chance that this premise is valid.
    """
    assert items_per_instant > 0
    assert cost_dim > 0
    assert target_delta + 1e-6 < 1
    assert target_delta - 1e-6 > 0

    values: List[List[float]] = [[random.random() for _ in range(items_per_instant)]
                                 for _ in range(n_instants)]
    if not mandatory_packing:
        for t in values:
            t.append(0.0)

    weights: List[List[List[float]]] = [[] for _ in range(n_instants)]

    for t in weights:
        for _ in range(items_per_instant):
            t.append([random.random() for _ in range(cost_dim)])
        if not mandatory_packing:
            t.append([0.0 for _ in range(cost_dim)])

    cap = _find_cap(target_delta, cost_dim)
    e = sqrt(log(cost_dim)/cap)
    return values.copy(), deepcopy(weights), cap, e


def generate_random_instance(n_instants: int, cost_dim: int, items_per_instant: int = 1,
                             mandatory_packing: bool = True) -> \
        Tuple[List[List[float]], List[List[List[float]]], float, float]:
    """Generates random values, costs and capacity for a Packing Problem instance.
    Instances generated here may not respect guarantees constraints.

    Parameters
    ----------
    n_instants : int
        Number of instants to be generated.
    cost_dim : int
        Dimension of the cost vectors to be generated.
    items_per_instant : int
        Number of items that should be available in each instant.
    mandatory_packing : bool
        If instance should enforce the need to always pack an item in every instant.

    Returns
    -------
    values : list of list of float
        A list containing, for each instant, a list with that instant item's values.
    costs : list of list of list of float
        A list containing, for each instant, a list with that instant item's cost vectors.
    cap : float
        A random problem capacity.
    e : float
        The best theorical epsilon for the generated problem.

    Notes
    -----
    Setting ``mandatory_packing=False`` will cause this function to add, for each instant,
    an extra item with :math:`value = 0` and :math:`cost = 0` for every dimension, allowing
    the player to pack that item when he wants to "do nothing" in some instant.
    """
    assert items_per_instant > 0
    assert cost_dim > 0

    values: List[List[float]] = [[random.random() for _ in range(items_per_instant)]
                                 for _ in range(n_instants)]
    if not mandatory_packing:
        for t in values:
            t.append(0.0)

    weights: List[List[List[float]]] = [[] for _ in range(n_instants)]

    for t in weights:
        for _ in range(items_per_instant):
            t.append([random.random() for _ in range(cost_dim)])
        if not mandatory_packing:
            t.append([0.0 for _ in range(cost_dim)])

    cap = random.random() * n_instants/2
    e = sqrt(log(cost_dim, 2)/cap)
    return values.copy(), deepcopy(weights), cap, e
