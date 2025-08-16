"""기본 가드레일"""


def allow_trade(rolling_sharpe: float, drawdown: float, dd_cap: float) -> bool:
    if rolling_sharpe < 0:
        return False
    if drawdown > dd_cap:
        return False
    return True
