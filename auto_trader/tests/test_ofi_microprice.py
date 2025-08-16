from auto_trader.features.ofi import ofi
from auto_trader.features.microprice import microprice


def test_ofi_and_microprice():
    prev = [(100, 1)]
    curr = [(101, 2)]
    assert ofi(prev, curr) > 0
    mp = microprice(100, 101, 1, 1)
    assert mp == 100.5
