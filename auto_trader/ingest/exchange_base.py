from abc import ABC, abstractmethod
from typing import Any

from ..libs.common.types import MarketState


class ExchangeBase(ABC):
    @abstractmethod
    async def stream(self) -> Any:
        """시장 데이터를 비동기 스트림으로 제공"""

    @abstractmethod
    async def snapshot(self) -> MarketState:
        """현재 스냅샷 반환"""
