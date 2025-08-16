from .broker_base import BrokerBase
from ..libs.common.types import OrderIntent, TradeFill


class BinanceBroker(BrokerBase):
    def send(self, intent: OrderIntent) -> TradeFill:  # pragma: no cover
        raise NotImplementedError("실브로커는 구현되지 않았습니다")
