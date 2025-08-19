from libs.common.types import OrderIntent, TradeFill
from .broker_paper import BrokerPaper


class ExecutionEngine:
    def __init__(self, broker=None):
        self.broker = broker or BrokerPaper()

    async def execute(self, intent: OrderIntent) -> TradeFill:
        return await self.broker.send(intent)
