import asyncio
from typing import AsyncIterator
from libs.common.types import MarketState
from .exchange_base import ExchangeBase


class BinanceSpot(ExchangeBase):
    """테스트용 더미 바이낸스 스팟 커넥터."""

    def __init__(self, symbol: str):
        self.symbol = symbol

    async def stream_market(self) -> AsyncIterator[MarketState]:
        bid = 100.0
        ask = 101.0
        while True:
            ms = MarketState(
                ts=0.0,
                symbol=self.symbol,
                best_bid=bid,
                best_ask=ask,
                spread=ask - bid,
                bids=[[bid, 1.0]],
                asks=[[ask, 1.0]],
            )
            yield ms
            await asyncio.sleep(0.1)
