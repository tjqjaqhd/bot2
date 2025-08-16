from ingest.orderbook_rebuilder import OrderBookRebuilder


def test_orderbook_rebuilder():
    ob = OrderBookRebuilder(depth=2)
    ob.apply_snapshot([[100, 1], [99, 1]], [[101, 1], [102, 1]])
    st = ob.state()
    assert st.best_bid == 100
    assert st.best_ask == 101
    assert len(st.bids) == 2
    ob.apply_diff([[100, 0], [98, 2]], [[101, 0], [103, 1]])
    st2 = ob.state()
    assert st2.best_bid == 99
    assert st2.best_ask == 102
