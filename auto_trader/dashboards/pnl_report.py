"""단순 PnL 리포트"""
from typing import List
from ..libs.common.types import PnlBreakdown


def summarize(pnls: List[PnlBreakdown]) -> dict:
    net = sum(p.net_pnl for p in pnls)
    return {"net_pnl": net, "trades": len(pnls)}
