from __future__ import annotations
from libs.common.types import MarketState, AgentResult
from .base import AgentBase


class ShockGate(AgentBase):
    name = "shock_gate"

    async def __call__(self, state: MarketState) -> AgentResult:
        return AgentResult(name=self.name, mu_hat=0.0, sigma2=1.0, cost_est=0.0)
