from ..libs.common.utils import spread as sp


def spread(bid: float, ask: float) -> float:
    return sp(bid, ask)
