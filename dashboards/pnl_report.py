from libs.common.types import PnlBreakdown


def summarize(pnls):
    net = sum(p.net_pnl for p in pnls)
    return {"net_pnl": net, "trades": len(pnls)}
