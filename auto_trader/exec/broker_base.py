from abc import ABC, abstractmethod
from ..libs.common.types import OrderIntent, TradeFill


class BrokerBase(ABC):
    @abstractmethod
    def send(self, intent: OrderIntent) -> TradeFill:
        ...
