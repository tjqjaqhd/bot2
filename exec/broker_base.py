from __future__ import annotations
from abc import ABC, abstractmethod
from libs.common.types import OrderIntent, TradeFill


class BrokerBase(ABC):
    @abstractmethod
    async def send(self, intent: OrderIntent) -> TradeFill:
        ...
