from __future__ import annotations


def guard(sharpe: float, drawdown: float, sharpe_th: float = 0.0, dd_cap: float = 0.1) -> tuple[float, bool]:
    size_factor = 1.0
    allow_new = True
    if sharpe < sharpe_th:
        size_factor *= 0.5
    if drawdown > dd_cap:
        size_factor *= 0.5
    if sharpe < sharpe_th and drawdown > dd_cap:
        allow_new = False
    return size_factor, allow_new
