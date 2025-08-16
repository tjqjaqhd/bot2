from libs.common.types import MarketState
from features.ofi import ofi_feature
from features.microprice import microprice_feature


def make_state(bid, ask):
    return MarketState(ts=0, symbol="x", best_bid=bid, best_ask=ask, spread=ask-bid, bids=[[bid,1]], asks=[[ask,1]])


def test_ofi_and_microprice():
    s1 = make_state(100,101)
    s2 = make_state(101,102)
    assert ofi_feature(s1,s2) != 0
    mp = microprice_feature(s2)
    assert mp > s2.best_bid and mp < s2.best_ask
