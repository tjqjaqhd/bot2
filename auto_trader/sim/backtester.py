"""이벤트 구동 백테스터 스켈레톤"""
from typing import Iterable, List

from ..libs.common.types import MarketState, PnlBreakdown
from ..agents.alpha_microstructure import MicrostructureAlpha
from ..router.meta_router import MetaRouter
from ..exec.broker_paper import PaperBroker
from ..exec.execution_engine import ExecutionEngine


def run(states: Iterable[MarketState]) -> List[PnlBreakdown]:
    agent = MicrostructureAlpha()
    router = MetaRouter()
    broker = PaperBroker()
    engine = ExecutionEngine(broker)
    pnls: List[PnlBreakdown] = []
    for ms in states:
        ar = agent.process(ms)
        decision = router.route([ar])
        if decision.edge_hat > 0:
            fill = engine.execute(decision, "buy", 1.0, ms.best_ask)
            pnl = PnlBreakdown(
                signal_pnl=ar.mu_hat,
                slippage_pnl=-fill.slip,
                fee_pnl=-fill.fees,
                hedge_cost_pnl=0.0,
                net_pnl=ar.mu_hat - fill.slip - fill.fees,
            )
            pnls.append(pnl)
    return pnls
