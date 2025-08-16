from __future__ import annotations
from libs.common.types import MarketState


def microprice(state: MarketState) -> float:
    bid_px, bid_sz = state.bids[0] if state.bids else (0.0, 0.0)
    ask_px, ask_sz = state.asks[0] if state.asks else (0.0, 0.0)
    denom = bid_sz + ask_sz
    if denom == 0:
        return (bid_px + ask_px) / 2 if (bid_px and ask_px) else 0.0
    return (ask_px * bid_sz + bid_px * ask_sz) / denom
