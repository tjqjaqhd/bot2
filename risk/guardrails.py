class GuardRails:
    """단순 손절/샤프 기반 가드레일."""

    def __init__(self, dd_limit: float = 0.1):
        self.dd_limit = dd_limit
        self.dd = 0.0

    def check(self, pnl: float) -> bool:
        self.dd = min(self.dd, pnl)
        return abs(self.dd) < self.dd_limit
