import asyncio
from libs.common.types import MarketState
from agents.alpha_microstructure import AlphaMicrostructure
from agents.alpha_derivatives import AlphaDerivatives
from agents.regime_bocpd import RegimeBOCPD


def test_agents():
    async def _run():
        st1 = MarketState(ts=0, symbol="BTC", best_bid=100, best_ask=101, spread=1, bids=[[100, 1]], asks=[[101, 1]])
        st2 = MarketState(ts=1, symbol="BTC", best_bid=101, best_ask=102, spread=1, bids=[[101, 2]], asks=[[102, 1]])
        am = AlphaMicrostructure()
        await am(st1)
        res = await am(st2)
        assert res.name == "alpha_microstructure"
        ad = AlphaDerivatives()
        res2 = await ad(st2)
        assert res2.name == "alpha_derivatives"
        regime = RegimeBOCPD(threshold=0.5)
        await regime(st1)
        r2 = await regime(st2)
        assert r2.meta["regime"] in {"range", "burst"}

    asyncio.run(_run())
