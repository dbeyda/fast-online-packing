"""Helper module that provides usable math functions.
"""
from typing import List, Union


def dot_product(a: List[Union[int, float]], b: List[Union[int, float]]) -> Union[int, float]:
    """Compute dot product between two vectors.

    Parameters
    ----------
    a : list of (float or int)
        First vector.
    b : list of (float or int)
        Second vector.

    Returns
    -------
    int or float
        The result of the dot product.

    Raises
    ------
    Exception
        If `a` and `b` have different lengths.

    """
    if len(a) != len(b):
        raise Exception(f"The two vectors must have the same length: len(a)={len(a)} != len(b)={len(b)}.")
    sum: float = 0.0
    for i in range(len(a)):
        sum += a[i] * b[i]
    return sum
