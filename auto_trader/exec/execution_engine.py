from ..libs.common.types import RouterDecision, OrderIntent, TradeFill
from .broker_base import BrokerBase


class ExecutionEngine:
    def __init__(self, broker: BrokerBase):
        self.broker = broker

    def execute(self, decision: RouterDecision, side: str, qty: float, price: float) -> TradeFill:
        intent = OrderIntent(side=side, qty=qty, price=price, mode="taker_pov")
        return self.broker.send(intent)
