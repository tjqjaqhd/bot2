from __future__ import annotations
from libs.common.types import OrderIntent, TradeFill, MarketState, PnlBreakdown
from .broker_base import BrokerBase


class BrokerPaper(BrokerBase):
    def __init__(self, fee: float = 0.0004, slip: float = 0.0005):
        self.fee = fee
        self.slip = slip
        self.state: MarketState | None = None

    def update_state(self, state: MarketState) -> None:
        self.state = state

    async def send(self, intent: OrderIntent) -> TradeFill:
        if self.state is None:
            raise RuntimeError("no market state")
        px = self.state.best_ask if intent.side == "buy" else self.state.best_bid
        slip_px = px * self.slip
        exec_px = px + slip_px if intent.side == "buy" else px - slip_px
        fees = abs(exec_px * intent.qty) * self.fee
        return TradeFill(ts=0.0, filled_qty=intent.qty, avg_px=exec_px, fees=fees, slip=slip_px)

    def breakdown(self, fill: TradeFill, intent: OrderIntent, ref_price: float) -> PnlBreakdown:
        signal_pnl = (ref_price - fill.avg_px) * fill.filled_qty if intent.side == "buy" else (fill.avg_px - ref_price) * fill.filled_qty
        return PnlBreakdown(
            signal_pnl=signal_pnl,
            slippage_pnl=-fill.slip * fill.filled_qty,
            fee_pnl=-fill.fees,
            hedge_cost_pnl=0.0,
            net_pnl=signal_pnl - fill.slip * fill.filled_qty - fill.fees,
        )
