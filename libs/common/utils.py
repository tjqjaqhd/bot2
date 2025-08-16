import numpy as np


def calc_microprice(bid_px: float, bid_sz: float, ask_px: float, ask_sz: float) -> float:
    """가중 미드프라이스 계산."""
    return (ask_px * bid_sz + bid_px * ask_sz) / (bid_sz + ask_sz)


def calc_ofi(prev_bids, prev_asks, bids, asks):
    """단순 OFI 계산. 레벨 1만 사용."""
    bid_px, bid_sz = bids[0]
    ask_px, ask_sz = asks[0]
    prev_bid_px, prev_bid_sz = prev_bids[0]
    prev_ask_px, prev_ask_sz = prev_asks[0]
    ofi = 0.0
    if bid_px >= prev_bid_px:
        ofi += bid_sz - prev_bid_sz
    else:
        ofi -= prev_bid_sz
    if ask_px <= prev_ask_px:
        ofi -= ask_sz - prev_ask_sz
    else:
        ofi += prev_ask_sz
    return ofi
