from libs.common.types import AgentResult, MarketState


class RegimeBOCPD:
    """단순 레짐 판별 더미."""

    def __init__(self):
        self.regime = "trend"

    async def __call__(self, state: MarketState) -> AgentResult:
        return AgentResult(name="regime_bocpd", mu_hat=0.0, sigma2=1.0, cost_est=0.0, meta={"regime": self.regime})
