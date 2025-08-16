from __future__ import annotations
from libs.common.types import MarketState, AgentResult


class AgentBase:
    name = "base"

    async def __call__(self, state: MarketState) -> AgentResult:
        raise NotImplementedError
