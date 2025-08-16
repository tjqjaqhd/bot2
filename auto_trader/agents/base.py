from abc import ABC, abstractmethod
from ..libs.common.types import AgentResult, MarketState


class AgentBase(ABC):
    name: str

    @abstractmethod
    def process(self, ms: MarketState) -> AgentResult:
        ...
