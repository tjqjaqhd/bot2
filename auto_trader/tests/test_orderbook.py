from auto_trader.ingest.orderbook_rebuilder import OrderbookRebuilder


def test_orderbook_rebuilder():
    ob = OrderbookRebuilder(depth=2)
    ob.apply_snapshot([[100, 1], [99, 1]], [[101, 1], [102, 1]])
    ob.apply_diff([[100, 2]], "bids")
    bids, asks = ob.top()
    assert bids[0] == (100, 2)
    assert asks[0] == (101, 1)
