from __future__ import annotations
from libs.common.types import RouterDecision, MarketState, OrderIntent, TradeFill
from .broker_base import BrokerBase


class ExecutionEngine:
    def __init__(self, broker: BrokerBase):
        self.broker = broker

    async def execute(self, decision: RouterDecision, state: MarketState, qty: float) -> TradeFill:
        side = "buy" if decision.edge_hat > 0 else "sell"
        intent = OrderIntent(side=side, qty=qty, mode="taker_pov")
        return await self.broker.send(intent)
