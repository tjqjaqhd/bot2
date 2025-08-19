import asyncio
from libs.common.types import OrderIntent
from exec.execution_engine import ExecutionEngine


def test_execution_engine_fill():
    engine = ExecutionEngine()
    intent = OrderIntent(side="buy", qty=1.0, mode="taker_pov", pov_cap=0.1)
    loop = asyncio.get_event_loop()
    fill = loop.run_until_complete(engine.execute(intent))
    assert fill.filled_qty == 1.0
