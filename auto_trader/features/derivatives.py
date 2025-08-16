"""파생 정보 파서 스텁"""
from ..libs.common.types import MarketState


def funding_signal(ms: MarketState) -> float:
    return ms.funding or 0.0


def oi_delta(ms_prev: MarketState, ms_curr: MarketState) -> float:
    if ms_prev.oi is None or ms_curr.oi is None:
        return 0.0
    return ms_curr.oi - ms_prev.oi
