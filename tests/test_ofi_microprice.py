from libs.common.types import MarketState
from features.ofi import compute_ofi
from features.microprice import microprice


def test_ofi_microprice():
    prev = MarketState(ts=0, symbol="BTC", best_bid=100, best_ask=101, spread=1, bids=[[100, 1]], asks=[[101, 1]])
    curr = MarketState(ts=1, symbol="BTC", best_bid=100, best_ask=101, spread=1, bids=[[100, 2]], asks=[[101, 0.5]])
    ofi_val = compute_ofi(prev, curr)
    assert ofi_val == 1.5
    mp = microprice(curr)
    assert round(mp, 1) == 100.8
