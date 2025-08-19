import asyncio
from libs.common.types import MarketState, OrderIntent
from agents.alpha_microstructure import AlphaMicrostructure
from agents.alpha_derivatives import AlphaDerivatives
from router.meta_router import MetaRouter
from exec.execution_engine import ExecutionEngine


def test_end_to_end_flow():
    s1 = MarketState(ts=0, symbol="x", best_bid=100, best_ask=101, spread=1, bids=[[100,1]], asks=[[101,1]])
    s2 = MarketState(ts=1, symbol="x", best_bid=101, best_ask=102, spread=1, bids=[[101,1]], asks=[[102,1]])
    alpha1 = AlphaMicrostructure(interval=30)
    alpha2 = AlphaDerivatives()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(alpha1(s1))
    ar1 = loop.run_until_complete(alpha1(s2))
    ar2 = loop.run_until_complete(alpha2(s2))
    router = MetaRouter(fee=0.0)
    decision = router.route([ar1, ar2])
    assert decision.contributors
    engine = ExecutionEngine()
    intent = OrderIntent(side="buy", qty=1.0, mode="maker_ladder")
    fill = loop.run_until_complete(engine.execute(intent))
    assert fill.filled_qty == 1.0
