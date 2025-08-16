from __future__ import annotations
from typing import List
from libs.common.types import MarketState


class OrderBookRebuilder:
    def __init__(self, depth: int = 5, symbol: str = "BTCUSDT"):
        self.depth = depth
        self.symbol = symbol
        self.bids: dict[float, float] = {}
        self.asks: dict[float, float] = {}

    def apply_snapshot(self, bids: List[List[float]], asks: List[List[float]]) -> None:
        self.bids = {p: q for p, q in bids if q > 0}
        self.asks = {p: q for p, q in asks if q > 0}

    def apply_diff(self, bids: List[List[float]], asks: List[List[float]]) -> None:
        for p, q in bids:
            if q == 0:
                self.bids.pop(p, None)
            else:
                self.bids[p] = q
        for p, q in asks:
            if q == 0:
                self.asks.pop(p, None)
            else:
                self.asks[p] = q

    def state(self) -> MarketState:
        bids_sorted = sorted(self.bids.items(), key=lambda x: -x[0])[: self.depth]
        asks_sorted = sorted(self.asks.items(), key=lambda x: x[0])[: self.depth]
        best_bid = bids_sorted[0][0] if bids_sorted else 0.0
        best_ask = asks_sorted[0][0] if asks_sorted else 0.0
        spread = best_ask - best_bid
        return MarketState(
            ts=0.0,
            symbol=self.symbol,
            best_bid=best_bid,
            best_ask=best_ask,
            spread=spread,
            bids=[[p, q] for p, q in bids_sorted],
            asks=[[p, q] for p, q in asks_sorted],
        )
