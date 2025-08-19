from libs.common.types import MarketState


def spread_feature(state: MarketState) -> float:
    return state.spread
