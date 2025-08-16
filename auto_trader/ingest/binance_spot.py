import asyncio
from typing import Any

from .exchange_base import ExchangeBase
from ..libs.common.types import MarketState


class BinanceSpot(ExchangeBase):
    async def stream(self) -> Any:
        while True:
            await asyncio.sleep(0.1)
            yield {"dummy": 1}

    async def snapshot(self) -> MarketState:
        return MarketState(
            ts=0.0,
            symbol="BTCUSDT",
            best_bid=100.0,
            best_ask=100.5,
            spread=0.5,
            bids=[[99.5, 1.0]],
            asks=[[100.5, 1.0]],
        )
