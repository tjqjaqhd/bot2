from libs.common.types import AgentResult, MarketState
from features.ofi import ofi_feature
from features.microprice import microprice_feature


class AlphaMicrostructure:
    """OFI와 마이크로프라이스 기반 단기 알파."""

    def __init__(self, interval: float):
        self.interval = interval
        self.prev_state: MarketState | None = None

    async def __call__(self, state: MarketState) -> AgentResult:
        if self.prev_state is None:
            self.prev_state = state
            return AgentResult(name="alpha_microstructure", mu_hat=0.0, sigma2=1.0, cost_est=0.0)
        ofi = ofi_feature(self.prev_state, state)
        mp = microprice_feature(state)
        mu = ofi * 0.001
        self.prev_state = state
        return AgentResult(
            name="alpha_microstructure",
            mu_hat=mu,
            sigma2=0.01,
            cost_est=0.0005,
            exec_profile={"microprice": mp},
        )
