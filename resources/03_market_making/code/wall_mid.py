"""
Module 03 — Wall-Mid (Timo Diehm) standalone implementation.
Re-derived from Timo's P3 round_1_strategy.py.

Run the self-test:
    python wall_mid.py
"""

from __future__ import annotations
import math
from typing import List, Optional, Tuple


def wall_mid_quotes(
    bids: List[Tuple[float, float]],
    asks: List[Tuple[float, float]],
    inventory: int,
    max_pos: int = 20,
    skew_per_unit: float = 0.2,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Place bid 1 tick inside the largest bid wall, ask 1 tick outside the largest ask wall.
    Skew both by inventory.

    bids: list of (price, volume) at the bid side, best first (highest price)
    asks: list of (price, volume) at the ask side, best first (lowest price)
    inventory: signed (positive = long)
    max_pos: hard inventory cap; halt one side when hit
    skew_per_unit: ticks of skew per unit of inventory

    Returns: (bid, ask) or (None, ask) etc.
    """
    if not bids or not asks:
        return None, None

    bid_wall = sorted(bids, key=lambda x: -x[1])[0][0]
    ask_wall = sorted(asks, key=lambda x: -x[1])[0][0]
    skew = inventory * skew_per_unit

    bid = bid_wall + 1 - skew
    ask = ask_wall - 1 - skew

    if inventory >= max_pos:
        bid = None
    if inventory <= -max_pos:
        ask = None

    # Crossed-book safety
    if bid is not None and ask is not None and bid >= ask:
        mid = (bid + ask) / 2
        bid, ask = mid - 0.5, mid + 0.5

    return bid, ask


def find_walls(
    bids: List[Tuple[float, float]],
    asks: List[Tuple[float, float]],
    multiplier: float = 3.0,
) -> Tuple[Optional[Tuple[float, float]], Optional[Tuple[float, float]]]:
    """Find the largest wall on each side. Wall = volume >= multiplier * median of top 3."""
    def _find_wall(book):
        if len(book) < 3:
            return None
        top3 = sorted(v for _, v in book[:3])
        median = top3[1]
        candidates = [(p, v) for p, v in book if v >= multiplier * median]
        if not candidates:
            return None
        return max(candidates, key=lambda x: x[1])

    return _find_wall(bids), _find_wall(asks)


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Symmetric book with one wall
    bids = [(99, 5), (98, 50), (97, 8)]   # wall at 98 (vol 50, 10x median)
    asks = [(101, 4), (102, 60), (103, 7)] # wall at 102 (vol 60)

    bid_wall, ask_wall = find_walls(bids, asks)
    print(f"Bid wall: {bid_wall}, Ask wall: {ask_wall}")
    assert bid_wall == (98, 50)
    assert ask_wall == (102, 60)

    # Quote at zero inventory
    bid, ask = wall_mid_quotes(bids, asks, inventory=0)
    print(f"Quote at inv=0: bid={bid}, ask={ask}")
    assert bid == 99 and ask == 101

    # Skew with inventory
    bid_long, ask_long = wall_mid_quotes(bids, asks, inventory=10)
    print(f"Quote at inv=10: bid={bid_long}, ask={ask_long}")
    # Skew = 10 * 0.2 = 2; bid = 99 - 2 = 97; ask = 101 - 2 = 99
    assert bid_long == 97 and ask_long == 99

    # Hard cap
    bid_cap, _ = wall_mid_quotes(bids, asks, inventory=20, max_pos=20)
    print(f"Capped at inv=20: bid={bid_cap}")
    assert bid_cap is None

    # Empty book safety
    empty = wall_mid_quotes([], [], inventory=0)
    print(f"Empty book: {empty}")
    assert empty == (None, None)

    print("All self-tests passed.")
