from __future__ import annotations
from libs.common.types import MarketState


def spread(state: MarketState) -> float:
    return state.best_ask - state.best_bid
