from __future__ import annotations
from typing import List, Dict
from libs.common.types import MarketState


class OrderbookRebuilder:
    """스냅샷+디프 기반 L2 재구성 (단순 버전)."""

    def __init__(self, depth: int = 1):
        self.depth = depth
        self.bids: Dict[float, float] = {}
        self.asks: Dict[float, float] = {}

    def apply_snapshot(self, bids: List[List[float]], asks: List[List[float]]):
        self.bids = {px: sz for px, sz in bids[: self.depth]}
        self.asks = {px: sz for px, sz in asks[: self.depth]}

    def apply_diff(self, bids: List[List[float]], asks: List[List[float]]):
        for px, sz in bids:
            if sz == 0:
                self.bids.pop(px, None)
            else:
                self.bids[px] = sz
        for px, sz in asks:
            if sz == 0:
                self.asks.pop(px, None)
            else:
                self.asks[px] = sz

    def snapshot(self) -> MarketState:
        bid_levels = sorted(self.bids.items(), reverse=True)[: self.depth]
        ask_levels = sorted(self.asks.items())[: self.depth]
        best_bid = bid_levels[0][0] if bid_levels else 0.0
        best_ask = ask_levels[0][0] if ask_levels else 0.0
        return MarketState(
            ts=0.0,
            symbol="",
            best_bid=best_bid,
            best_ask=best_ask,
            spread=best_ask - best_bid,
            bids=[[px, sz] for px, sz in bid_levels],
            asks=[[px, sz] for px, sz in ask_levels],
        )
