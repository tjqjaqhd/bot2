from __future__ import annotations
from typing import List
from libs.common.types import MarketState
from agents.base import AgentBase
from router.meta_router import MetaRouter
from exec.execution_engine import ExecutionEngine
from exec.broker_paper import BrokerPaper


class Backtester:
    def __init__(self, agent: AgentBase):
        self.agent = agent
        self.router = MetaRouter()
        self.broker = BrokerPaper()
        self.engine = ExecutionEngine(self.broker)

    async def run(self, states: List[MarketState]):
        fills = []
        for st in states:
            self.broker.update_state(st)
            res = await self.agent(st)
            decision = self.router.decide([res])
            fill = await self.engine.execute(decision, st, qty=1)
            fills.append(fill)
        return fills
