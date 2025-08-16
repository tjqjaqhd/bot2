from ..libs.common.utils import microprice as mp


def microprice(bid_px: float, ask_px: float, bid_size: float, ask_size: float) -> float:
    return mp(bid_px, ask_px, bid_size, ask_size)
