from typing import Iterable, List
from libs.common.types import MarketState, AgentResult, RouterDecision
from router.meta_router import MetaRouter


class Backtester:
    def __init__(self, agents: List, router: MetaRouter):
        self.agents = agents
        self.router = router

    async def run(self, stream: Iterable[MarketState]):
        decisions = []
        async for state in stream:  # pragma: no cover - 단순 구조
            ars: List[AgentResult] = []
            for ag in self.agents:
                ars.append(await ag(state))
            decision = self.router.route(ars)
            decisions.append(decision)
        return decisions
