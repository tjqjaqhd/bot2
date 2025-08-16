from __future__ import annotations

import numpy as np


def midprice(best_bid: float, best_ask: float) -> float:
    """단순 미드프라이스 계산"""
    return (best_bid + best_ask) / 2


def spread(best_bid: float, best_ask: float) -> float:
    return best_ask - best_bid


def microprice(best_bid: float, best_ask: float, bid_size: float, ask_size: float) -> float:
    return (best_bid * ask_size + best_ask * bid_size) / (bid_size + ask_size)


def np_var(x: np.ndarray) -> float:
    return float(np.var(x))
