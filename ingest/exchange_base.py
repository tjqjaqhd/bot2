from __future__ import annotations
from abc import ABC, abstractmethod
from typing import AsyncIterator
from libs.common.types import MarketState


class ExchangeBase(ABC):
    @abstractmethod
    async def market_stream(self) -> AsyncIterator[MarketState]:
        ...
