from libs.common.utils import calc_ofi
from libs.common.types import MarketState


def ofi_feature(prev: MarketState, cur: MarketState) -> float:
    return calc_ofi(prev.bids, prev.asks, cur.bids, cur.asks)
