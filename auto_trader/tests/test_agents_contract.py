from auto_trader.agents.alpha_microstructure import MicrostructureAlpha
from auto_trader.agents.alpha_derivatives import DerivativesAlpha
from auto_trader.libs.common.types import MarketState


def dummy_ms():
    return MarketState(
        ts=0.0,
        symbol="BTCUSDT",
        best_bid=100,
        best_ask=101,
        spread=1,
        bids=[[100, 1]],
        asks=[[101, 1]],
    )


def test_agents():
    ms = dummy_ms()
    m = MicrostructureAlpha()
    d = DerivativesAlpha()
    assert m.process(ms).mu_hat == 0.0
    assert d.process(ms).name == "alpha_deriv"
