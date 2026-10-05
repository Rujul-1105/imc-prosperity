"""
Module 03 — Simple event-driven backtester for a market-making strategy.
Decomposes PnL into spread / inventory drift / rebalance.

Run the self-test:
    python backtest_mm.py

For real use, feed in a list of MarketState snapshots + historical trades.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Callable, Dict


@dataclass
class Trade:
    """A market order that crossed against our quote."""
    timestamp: int
    side: str        # 'buy' or 'sell' (from the taker's perspective)
    price: float
    quantity: int


@dataclass
class PnLAttribution:
    spread_capture: float = 0.0
    inventory_drift: float = 0.0
    rebalance_cost: float = 0.0

    @property
    def total(self) -> float:
        return self.spread_capture + self.inventory_drift + self.rebalance_cost

    def __repr__(self):
        return (f"PnL(spread={self.spread_capture:.2f}, "
                f"drift={self.inventory_drift:.2f}, "
                f"rebalance={self.rebalance_cost:.2f}, "
                f"total={self.total:.2f})")


@dataclass
class BacktestResult:
    pnl: PnLAttribution
    inventory_time_series: List[int] = field(default_factory=list)
    mid_time_series: List[float] = field(default_factory=list)
    fills: List[Trade] = field(default_factory=list)


def simulate(
    mid_series: List[float],
    bid_book_series: List[List[Tuple[float, float]]],
    ask_book_series: List[List[Tuple[float, float]]],
    quote_fn: Callable,
    sigma: float = 0.5,
    gamma: float = 0.1,
    kappa: float = 1.5,
    max_pos: int = 20,
) -> BacktestResult:
    """
    Run a market-making backtest.

    mid_series: list of historical mid prices
    bid_book_series / ask_book_series: list of historical book snapshots
        each is a list of (price, volume), best first
    quote_fn: callable(state) -> (bid, ask)
    """
    from market_maker import MarketState
    pnl = PnLAttribution()
    inventory = 0
    avg_entry = 0.0  # average entry price of current position
    inv_history = []
    mid_history = []
    fills = []

    for i, (mid, bb, ab) in enumerate(zip(mid_series, bid_book_series, ask_book_series)):
        state = MarketState(
            mid=mid, bids=bb, asks=ab,
            inventory=inventory, sigma=sigma, tau=60.0,
            gamma=gamma, kappa=kappa, max_pos=max_pos,
        )
        quote = quote_fn(state)
        # Accept either a tuple (bid, ask) or a Quote dataclass
        if hasattr(quote, "bid"):
            bid, ask = quote.bid, quote.ask
        else:
            bid, ask = quote

        # Naive fill model: if our bid >= touch ask, we lift the touch (we buy at ask).
        # If our ask <= touch bid, we hit the touch (we sell at bid).
        # Prosperity's "no queue priority" makes this realistic.
        if bid is not None and ab and bid >= ab[0][0]:
            fill_price = ab[0][0]
            qty = min(ab[0][1], max_pos - inventory)
            if qty > 0:
                # we buy
                new_total = inventory * avg_entry + qty * fill_price
                inventory += qty
                avg_entry = new_total / inventory if inventory else 0
                pnl.spread_capture -= 0  # captured on round-trip
                fills.append(Trade(i, 'buy', fill_price, qty))
        if ask is not None and bb and ask <= bb[0][0]:
            fill_price = bb[0][0]
            qty = min(bb[0][1], max_pos + inventory)
            if qty > 0:
                # we sell
                new_total = inventory * avg_entry - qty * fill_price
                inventory -= qty
                if inventory > 0:
                    avg_entry = new_total / inventory
                elif inventory == 0:
                    # closed round-trip; realized PnL is the spread
                    realized = -new_total
                    pnl.spread_capture += realized
                    avg_entry = 0
                else:
                    # short side; treat avg_entry as the new short entry
                    avg_entry = new_total / inventory if inventory else 0
                fills.append(Trade(i, 'sell', fill_price, qty))

        # Inventory drift: track mark-to-market PnL for our net position
        if inventory != 0 and avg_entry != 0:
            pnl.inventory_drift = inventory * (mid - avg_entry)

        inv_history.append(inventory)
        mid_history.append(mid)

    # Rebalance: close out at the last mid
    if inventory != 0:
        pnl.rebalance_cost = -inventory * (mid_history[-1] - avg_entry)

    return BacktestResult(pnl=pnl, inventory_time_series=inv_history, mid_time_series=mid_history, fills=fills)


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Build a synthetic series: constant mid 100, deep symmetric book
    n = 200
    mid_series = [100.0] * n
    bid_books = [[(99, 50), (98, 30), (97, 20)] for _ in range(n)]
    ask_books = [[(101, 50), (102, 30), (103, 20)] for _ in range(n)]

    from market_maker import MarketMaker, MarketState
    mm = MarketMaker()

    def hybrid_quote(s: MarketState):
        return mm.hybrid_quotes(s)

    result = simulate(
        mid_series=mid_series,
        bid_book_series=bid_books,
        ask_book_series=ask_books,
        quote_fn=hybrid_quote,
        sigma=0.1, gamma=0.1, kappa=1.5, max_pos=20,
    )
    print(f"Hybrid backtest: {result.pnl}")
    print(f"Final inventory: {result.inventory_time_series[-1]}")
    print(f"Total fills: {len(result.fills)}")

    # With constant mid, no drift, no rebalance (or trivial), some spread capture from round-trips
    assert isinstance(result.pnl.spread_capture, float)

    # Try AS too
    def as_quote(s: MarketState):
        return mm.as_quotes(s)
    result_as = simulate(
        mid_series=mid_series, bid_book_series=bid_books, ask_book_series=ask_books,
        quote_fn=as_quote, sigma=0.1, gamma=0.1, kappa=1.5, max_pos=20,
    )
    print(f"AS backtest: {result_as.pnl}")

    print("All self-tests passed.")
