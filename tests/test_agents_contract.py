import asyncio
from libs.common.types import MarketState, AgentResult
from agents.alpha_microstructure import AlphaMicrostructure
from agents.alpha_derivatives import AlphaDerivatives


def test_agents_return_agentresult():
    s = MarketState(ts=0, symbol="x", best_bid=100, best_ask=101, spread=1, bids=[[100,1]], asks=[[101,1]])
    alpha1 = AlphaMicrostructure(interval=30)
    alpha2 = AlphaDerivatives()
    loop = asyncio.get_event_loop()
    res1 = loop.run_until_complete(alpha1(s))
    res2 = loop.run_until_complete(alpha2(s))
    assert isinstance(res1, AgentResult)
    assert isinstance(res2, AgentResult)
