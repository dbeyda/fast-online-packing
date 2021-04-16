from typing import List, Union


def dot_product(a: List[Union[int, float]], b: List[Union[int, float]]) -> Union[int, float]:
    if len(a) != len(b):
        raise Exception(f"The two vectors must have the same length: len(a)={len(a)} != len(b)={len(b)}.")
    sum: float = 0.0
    for i in range(len(a)):
        sum += a[i] * b[i]
    return sum
