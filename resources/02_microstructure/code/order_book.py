"""
Module 02 — Microstructure
Toy order book class used by exercises in this module.

Run the self-test:
    python order_book.py
"""

from __future__ import annotations
from typing import List, Optional, Tuple

Price = float
Volume = int
Level = Tuple[Price, Volume]


class OrderBook:
    """A toy L2-style order book: top-of-book plus deeper levels.

    Bids are stored as a list of (price, volume) sorted DESCENDING by price.
    Asks are stored as a list of (price, volume) sorted ASCENDING by price.
    Both lists are kept sorted after every insertion.
    """

    def __init__(self, bids: Optional[List[Level]] = None, asks: Optional[List[Level]] = None):
        self.bids: List[Level] = sorted(bids or [], key=lambda x: -x[0])
        self.asks: List[Level] = sorted(asks or [], key=lambda x: x[0])

    # ------------------------------------------------------------------ basics

    @property
    def best_bid(self) -> Optional[Price]:
        return self.bids[0][0] if self.bids else None

    @property
    def best_ask(self) -> Optional[Price]:
        return self.asks[0][0] if self.asks else None

    @property
    def bid_volume(self) -> Volume:
        return self.bids[0][1] if self.bids else 0

    @property
    def ask_volume(self) -> Volume:
        return self.asks[0][1] if self.asks else 0

    @property
    def mid(self) -> Optional[Price]:
        bb, ba = self.best_bid, self.best_ask
        return (bb + ba) / 2 if (bb is not None and ba is not None) else None

    @property
    def spread(self) -> Optional[Price]:
        bb, ba = self.best_bid, self.best_ask
        return (ba - bb) if (bb is not None and ba is not None) else None

    @property
    def microprice(self) -> Optional[Price]:
        bb, ba = self.best_bid, self.best_ask
        vb, va = self.bid_volume, self.ask_volume
        if bb is None or ba is None or (vb + va) == 0:
            return None
        return (vb * ba + va * bb) / (vb + va)

    # ----------------------------------------------------------------- structure

    def cum_depth(self, side: str, levels: int) -> Volume:
        """Cumulative volume in the top N levels of one side. side in {'bid','ask'}."""
        book = self.bids if side == "bid" else self.asks
        return sum(v for _, v in book[:levels])

    def wall_volume(self, side: str, multiplier: float = 3.0) -> Optional[Level]:
        """Find the largest single-level wall. A wall is a level whose volume
        exceeds `multiplier` times the median of the top-3 levels on that side."""
        book = self.bids if side == "bid" else self.asks
        if len(book) < 3:
            return None
        top3 = [v for _, v in book[:3]]
        median = sorted(top3)[1]
        walls = [(p, v) for p, v in book if v >= multiplier * median]
        if not walls:
            return None
        # Return the wall with the highest volume
        return max(walls, key=lambda x: x[1])

    # ----------------------------------------------------------- mutation helpers

    def insert(self, side: str, price: Price, volume: Volume) -> None:
        """Insert or replace a level on one side. Volume 0 removes the level."""
        book = self.bids if side == "bid" else self.asks
        # remove existing level at this price
        book[:] = [(p, v) for p, v in book if p != price]
        if volume > 0:
            book.append((price, volume))
        if side == "bid":
            book.sort(key=lambda x: -x[0])
        else:
            book.sort(key=lambda x: x[0])

    def fill(self, side: str, price: Price, qty: Volume) -> Volume:
        """Simulate a fill: take up to `qty` volume from the level at `price` on `side`.
        Returns the actual filled quantity (may be less if not enough depth)."""
        book = self.bids if side == "bid" else self.asks
        for i, (p, v) in enumerate(book):
            if p == price:
                taken = min(v, qty)
                book[i] = (p, v - taken)
                if book[i][1] == 0:
                    del book[i]
                return taken
        return 0

    # --------------------------------------------------------------- diagnostics

    def to_dict(self) -> dict:
        return {
            "best_bid": self.best_bid,
            "best_ask": self.best_ask,
            "mid": self.mid,
            "spread": self.spread,
            "microprice": self.microprice,
            "bid_volume": self.bid_volume,
            "ask_volume": self.ask_volume,
        }

    def __repr__(self) -> str:
        bb = f"{self.best_bid}@{self.bid_volume}" if self.bids else "—"
        ba = f"{self.best_ask}@{self.ask_volume}" if self.asks else "—"
        return f"OrderBook(bid={bb}, ask={ba}, mid={self.mid}, spread={self.spread})"


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Toy book: bid at 99 with 10, ask at 101 with 20
    book = OrderBook(bids=[(99, 10)], asks=[(101, 20)])
    print("Initial:", book)
    assert book.mid == 100.0
    assert book.spread == 2.0
    assert abs(book.microprice - (10 * 101 + 20 * 99) / 30) < 1e-9   # 100.333...

    # Insert deeper levels
    book.insert("bid", 98, 50)
    book.insert("ask", 102, 5)
    print("After deeper levels:", book)
    assert book.cum_depth("bid", 2) == 60
    assert book.cum_depth("ask", 2) == 25

    # Fill part of the best bid
    taken = book.fill("bid", 99, 4)
    print(f"Fill 4 @ 99: took {taken}, remaining bid_vol={book.bid_volume}")
    assert taken == 4
    assert book.bid_volume == 6

    # Wall detection: artificially large wall
    book.insert("ask", 100, 200)  # massive wall
    wall = book.wall_volume("ask", multiplier=3.0)
    print("Largest ask wall:", wall)
    assert wall == (100, 200)

    # Removing a level
    book.insert("bid", 99, 0)
    assert book.best_bid == 98

    print("All self-tests passed.")
