"""간단한 L2 오더북 재구성"""
from typing import List, Tuple


class OrderbookRebuilder:
    def __init__(self, depth: int = 2):
        self.depth = depth
        self.bids: List[Tuple[float, float]] = []
        self.asks: List[Tuple[float, float]] = []

    def apply_snapshot(self, bids: List[List[float]], asks: List[List[float]]):
        self.bids = [(p, q) for p, q in bids[: self.depth]]
        self.asks = [(p, q) for p, q in asks[: self.depth]]

    def apply_diff(self, updates: List[List[float]], side: str):
        book = self.bids if side == "bids" else self.asks
        for price, qty in updates:
            for i, (p, _) in enumerate(book):
                if p == price:
                    if qty == 0:
                        book.pop(i)
                    else:
                        book[i] = (price, qty)
                    break
            else:
                if qty > 0:
                    book.append((price, qty))
        book.sort(reverse=(side == "bids"))
        del book[self.depth :]

    def top(self):
        return self.bids, self.asks
