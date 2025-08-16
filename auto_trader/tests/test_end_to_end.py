from auto_trader.libs.common.types import MarketState
from auto_trader.sim.backtester import run


def test_backtester():
    states = [
        MarketState(ts=i, symbol="BTCUSDT", best_bid=100+i, best_ask=101+i, spread=1,
                    bids=[[100+i,1]], asks=[[101+i,1]])
        for i in range(3)
    ]
    pnls = run(states)
    assert isinstance(pnls, list)
