from __future__ import annotations
from libs.common.types import MarketState, AgentResult
from .base import AgentBase
from features.ofi import compute_ofi
from features.microprice import microprice


class AlphaMicrostructure(AgentBase):
    name = "alpha_microstructure"

    def __init__(self):
        self.prev: MarketState | None = None

    async def __call__(self, state: MarketState) -> AgentResult:
        if self.prev is None:
            self.prev = state
            return AgentResult(name=self.name, mu_hat=0.0, sigma2=1.0, cost_est=state.spread / 2)
        ofi_val = compute_ofi(self.prev, state)
        mp = microprice(state)
        mu_hat = ofi_val * 0.001
        sigma2 = abs(ofi_val) * 0.01 + 1e-6
        cost_est = state.spread / 2
        self.prev = state
        return AgentResult(name=self.name, mu_hat=mu_hat, sigma2=sigma2, cost_est=cost_est, meta={"microprice": mp})
