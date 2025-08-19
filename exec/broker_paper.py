import time
from libs.common.types import OrderIntent, TradeFill, PnlBreakdown


class BrokerPaper:
    fee_rate = 0.0004

    async def send(self, intent: OrderIntent) -> TradeFill:
        px = intent.price or 100.0
        qty = intent.qty
        fees = abs(px * qty) * self.fee_rate
        slip = 0.0
        return TradeFill(ts=time.time(), filled_qty=qty, avg_px=px, fees=fees, slip=slip)

    def pnl_breakdown(self, entry_px: float, exit_px: float, qty: float, fees: float) -> PnlBreakdown:
        signal = (exit_px - entry_px) * qty
        return PnlBreakdown(signal_pnl=signal, slippage_pnl=0.0, fee_pnl=-fees, hedge_cost_pnl=0.0, net_pnl=signal - fees)
