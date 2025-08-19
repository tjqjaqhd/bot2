from .broker_base import BrokerBase
from libs.common.types import OrderIntent, TradeFill


class BrokerBinance(BrokerBase):
    """실제 바이낸스 브로커 스텁."""

    async def send(self, intent: OrderIntent) -> TradeFill:  # pragma: no cover
        raise NotImplementedError("실브로커는 구현되지 않았습니다")
