from __future__ import annotations
from libs.common.types import OrderIntent, TradeFill
from .broker_base import BrokerBase


class BrokerBinance(BrokerBase):
    async def send(self, intent: OrderIntent) -> TradeFill:
        raise NotImplementedError("실 브로커는 구현 필요")
