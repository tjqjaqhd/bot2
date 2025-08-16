from libs.common.types import AgentResult, MarketState


class AgentBase:
    name: str

    def __init__(self, name: str):
        self.name = name

    async def __call__(self, state: MarketState) -> AgentResult:
        raise NotImplementedError
