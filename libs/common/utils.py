from __future__ import annotations
from typing import List


def mid_price(bid: float, ask: float) -> float:
    return (bid + ask) / 2.0


def top_of_book(bids: List[List[float]], asks: List[List[float]]) -> tuple[float, float]:
    best_bid = bids[0][0] if bids else 0.0
    best_ask = asks[0][0] if asks else 0.0
    return best_bid, best_ask
