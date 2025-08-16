from __future__ import annotations
from typing import AsyncIterator
from .exchange_base import ExchangeBase
from libs.common.types import MarketState


class BinanceSpot(ExchangeBase):
    async def market_stream(self) -> AsyncIterator[MarketState]:
        if False:
            yield
        return
