from __future__ import annotations
from libs.common.types import MarketState


def parse_derivatives(state: MarketState) -> dict:
    return {
        "funding": state.funding or 0.0,
        "oi": state.oi or 0.0,
    }
