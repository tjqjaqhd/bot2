from __future__ import annotations
from libs.common.types import MarketState, AgentResult
from .base import AgentBase


class RegimeBOCPD(AgentBase):
    name = "regime_bocpd"

    def __init__(self, threshold: float = 50.0):
        self.prev_price: float | None = None
        self.regime = "range"
        self.threshold = threshold

    async def __call__(self, state: MarketState) -> AgentResult:
        mid = (state.best_bid + state.best_ask) / 2
        if self.prev_price is None:
            self.prev_price = mid
            return AgentResult(name=self.name, mu_hat=0.0, sigma2=1.0, cost_est=0.0, meta={"regime": self.regime})
        if abs(mid - self.prev_price) > self.threshold:
            self.regime = "burst"
        else:
            self.regime = "range"
        self.prev_price = mid
        return AgentResult(name=self.name, mu_hat=0.0, sigma2=1.0, cost_est=0.0, meta={"regime": self.regime})
