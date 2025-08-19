from libs.common.types import MarketState


def funding_basis_feature(state: MarketState) -> float:
    if state.funding is None or state.oi is None:
        return 0.0
    return state.funding * state.oi
