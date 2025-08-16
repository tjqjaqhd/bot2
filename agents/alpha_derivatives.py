from __future__ import annotations
from libs.common.types import MarketState, AgentResult
from .base import AgentBase


class AlphaDerivatives(AgentBase):
    name = "alpha_derivatives"

    async def __call__(self, state: MarketState) -> AgentResult:
        score = (state.funding or 0.0) + (state.oi or 0.0)
        mu_hat = score * 0.001
        sigma2 = abs(mu_hat) + 1e-6
        cost_est = state.spread / 2
        return AgentResult(name=self.name, mu_hat=mu_hat, sigma2=sigma2, cost_est=cost_est)
