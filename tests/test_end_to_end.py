import asyncio
from libs.common.types import MarketState
from agents.alpha_microstructure import AlphaMicrostructure
from sim.backtester import Backtester


def test_backtester():
    async def _run():
        states = [
            MarketState(ts=0, symbol="BTC", best_bid=100, best_ask=101, spread=1, bids=[[100, 1]], asks=[[101, 1]]),
            MarketState(ts=1, symbol="BTC", best_bid=101, best_ask=102, spread=1, bids=[[101, 2]], asks=[[102, 1]]),
        ]
        bt = Backtester(AlphaMicrostructure())
        fills = await bt.run(states)
        assert len(fills) == len(states)

    asyncio.run(_run())
