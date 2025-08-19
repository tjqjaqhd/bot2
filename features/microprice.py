from libs.common.utils import calc_microprice
from libs.common.types import MarketState


def microprice_feature(state: MarketState) -> float:
    bid_px, bid_sz = state.bids[0]
    ask_px, ask_sz = state.asks[0]
    return calc_microprice(bid_px, bid_sz, ask_px, ask_sz)
