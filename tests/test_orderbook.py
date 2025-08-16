from ingest.orderbook_rebuilder import OrderbookRebuilder


def test_rebuilder_snapshot_and_diff():
    ob = OrderbookRebuilder(depth=1)
    ob.apply_snapshot([[100, 1]], [[101, 1]])
    state = ob.snapshot()
    assert state.best_bid == 100
    ob.apply_diff([[100, 0]], [[101, 2]])
    state = ob.snapshot()
    assert state.best_ask == 101 and state.asks[0][1] == 2
