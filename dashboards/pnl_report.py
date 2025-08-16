from __future__ import annotations
from typing import List
from libs.common.types import PnlBreakdown


def summary(breakdowns: List[PnlBreakdown]) -> dict:
    net = sum(b.net_pnl for b in breakdowns)
    signal = sum(b.signal_pnl for b in breakdowns)
    slip = sum(b.slippage_pnl for b in breakdowns)
    fee = sum(b.fee_pnl for b in breakdowns)
    return {"net": net, "signal": signal, "slip": slip, "fee": fee}
