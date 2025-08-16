from __future__ import annotations
from libs.common.types import MarketState


def compute_ofi(prev: MarketState, curr: MarketState) -> float:
    prev_bid = prev.bids[0][1] if prev.bids else 0.0
    prev_ask = prev.asks[0][1] if prev.asks else 0.0
    curr_bid = curr.bids[0][1] if curr.bids else 0.0
    curr_ask = curr.asks[0][1] if curr.asks else 0.0
    return (curr_bid - prev_bid) - (curr_ask - prev_ask)
