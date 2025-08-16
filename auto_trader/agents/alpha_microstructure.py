"""OFI와 마이크로프라이스 기반 단기 알파"""
from typing import Optional

from .base import AgentBase
from ..libs.common.types import AgentResult, MarketState
from ..features.ofi import ofi
from ..features.microprice import microprice


class MicrostructureAlpha(AgentBase):
    name = "alpha_micro"

    def __init__(self):
        self.prev: Optional[MarketState] = None

    def process(self, ms: MarketState) -> AgentResult:
        if self.prev is None:
            self.prev = ms
            return AgentResult(name=self.name, mu_hat=0.0, sigma2=1.0, cost_est=0.0)
        bid_prev, ask_prev = self.prev.bids[0], self.prev.asks[0]
        bid_curr, ask_curr = ms.bids[0], ms.asks[0]
        ofi_val = ofi([tuple(bid_prev)], [tuple(bid_curr)]) - ofi([tuple(ask_prev)], [tuple(ask_curr)])
        mp = microprice(ms.bids[0][0], ms.asks[0][0], ms.bids[0][1], ms.asks[0][1])
        mu = ofi_val * 0.001 + (mp - (ms.best_bid + ms.best_ask) / 2)
        res = AgentResult(name=self.name, mu_hat=mu, sigma2=1.0, cost_est=0.01)
        self.prev = ms
        return res
