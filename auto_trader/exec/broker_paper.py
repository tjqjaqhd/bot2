import time
from .broker_base import BrokerBase
from ..libs.common.types import OrderIntent, TradeFill


class PaperBroker(BrokerBase):
    fee = 0.0004

    def send(self, intent: OrderIntent) -> TradeFill:
        slip = 0.5 * self.fee * intent.qty
        avg_px = intent.price or 0.0
        fees = avg_px * self.fee * intent.qty
        return TradeFill(ts=time.time(), filled_qty=intent.qty, avg_px=avg_px, fees=fees, slip=slip)
