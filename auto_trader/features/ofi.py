"""주문흐름 불균형(OFI)"""
from typing import List, Tuple


def ofi(prev: List[Tuple[float, float]], curr: List[Tuple[float, float]]) -> float:
    diff = 0.0
    for (p, q), (p2, q2) in zip(prev, curr):
        diff += (q2 - q) if p2 >= p else -(q - q2)
    return diff
