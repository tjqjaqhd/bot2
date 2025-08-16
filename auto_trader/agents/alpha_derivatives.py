from typing import Optional

from .base import AgentBase
from ..libs.common.types import AgentResult, MarketState
from ..features.derivatives import funding_signal


class DerivativesAlpha(AgentBase):
    name = "alpha_deriv"

    def __init__(self):
        self.prev: Optional[MarketState] = None

    def process(self, ms: MarketState) -> AgentResult:
        mu = funding_signal(ms) * 0.1
        return AgentResult(name=self.name, mu_hat=mu, sigma2=1.0, cost_est=0.01)
