from libs.common.types import AgentResult, MarketState
from features.derivatives import funding_basis_feature


class AlphaDerivatives:
    def __init__(self):
        pass

    async def __call__(self, state: MarketState) -> AgentResult:
        score = funding_basis_feature(state)
        mu = score * 0.0001
        return AgentResult(
            name="alpha_derivatives",
            mu_hat=mu,
            sigma2=0.02,
            cost_est=0.0005,
            meta={"score": score},
        )
