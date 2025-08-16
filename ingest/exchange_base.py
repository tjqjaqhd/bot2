from abc import ABC, abstractmethod
from typing import AsyncIterator
from libs.common.types import MarketState


class ExchangeBase(ABC):
    symbol: str

    @abstractmethod
    async def stream_market(self) -> AsyncIterator[MarketState]:
        ...
