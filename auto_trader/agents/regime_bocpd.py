"""간단한 레짐 게이트"""
from ..libs.common.types import MarketState


class RegimeBOCPD:
    def __init__(self):
        self.prev_price: float | None = None
        self.regime = "range"

    def update(self, ms: MarketState) -> str:
        mid = (ms.best_bid + ms.best_ask) / 2
        if self.prev_price is not None:
            if mid > self.prev_price:
                self.regime = "trend"
            elif mid < self.prev_price:
                self.regime = "range"
        self.prev_price = mid
        return self.regime
