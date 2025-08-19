from libs.common.types import AgentResult, MarketState


class ShockGate:
    """외부 이벤트 게이트 더미."""

    def __init__(self):
        pass

    async def __call__(self, state: MarketState) -> AgentResult:
        return AgentResult(name="shock_gate", mu_hat=0.0, sigma2=1.0, cost_est=0.0)
