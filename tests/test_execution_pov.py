import asyncio
from libs.common.types import MarketState, RouterDecision
from exec.broker_paper import BrokerPaper
from exec.execution_engine import ExecutionEngine


def test_execution_engine():
    async def _run():
        state = MarketState(ts=0, symbol="BTC", best_bid=100, best_ask=101, spread=1, bids=[[100, 1]], asks=[[101, 1]])
        broker = BrokerPaper()
        broker.update_state(state)
        engine = ExecutionEngine(broker)
        decision = RouterDecision(edge_hat=1.0, contributors=[], regime="neutral")
        fill = await engine.execute(decision, state, qty=1)
        assert fill.filled_qty == 1
        assert fill.avg_px > 100

    asyncio.run(_run())
