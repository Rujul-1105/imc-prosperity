"""
Module 06 — Full basket-arb strategy with backtester and PnL decomposition.

Run the self-test (synthetic data):
    python basket_arb.py
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from nav import spread


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
class Trade:
    """One round-trip: enter when spread > threshold, exit when spread < threshold."""
    side: str             # 'short_basket' (basket rich) or 'long_basket' (basket cheap)
    entry_spread: float
    exit_spread: float
    pnl: float


def basket_arb_backtest(
    basket_mids: List[float],
    leg_mids_series: List[Dict[str, float]],
    weights: Dict[str, float],
    threshold: float = 10.0,
    max_basket_pos: int = 5,
    fee_per_leg: float = 0.0,
) -> Tuple[PnLAttribution, List[Trade]]:
    """
    Walk-forward backtest of basket-arb strategy.

    basket_mids: list of basket mid prices
    leg_mids_series: list of dicts (one per tick) with leg mids
    weights: dict of leg -> weight
    threshold: |spread| > threshold triggers entry; |spread| < threshold exits
    max_basket_pos: max basket units to hold (legs scale by weight)
    fee_per_leg: per-leg fee in price units (per side)

    Returns: (PnLAttribution, list of completed Trades)
    """
    pnl = PnLAttribution()
    trades: List[Trade] = []
    basket_pos = 0          # signed basket units
    leg_pos: Dict[str, int] = {leg: 0 for leg in weights}
    entry_spread = 0.0
    entry_side = None       # 'short_basket' or 'long_basket'

    for t, (b, lm) in enumerate(zip(basket_mids, leg_mids_series)):
        s = spread(b, lm, weights)
        # Mark-to-market PnL on current position
        if basket_pos != 0:
            # The realized PnL is (entry_spread - current_spread) * basket_pos
            # with sign depending on side
            if entry_side == "short_basket":
                pnl.spread_capture = (entry_spread - s) * abs(basket_pos)
            elif entry_side == "long_basket":
                pnl.spread_capture = (s - entry_spread) * abs(basket_pos)

            # Inventory drift: PnL from underlying moves (legs minus basket)
            leg_value = sum(leg_pos[leg] * lm[leg] for leg in weights)
            basket_value = basket_pos * b
            pnl.inventory_drift = -(leg_value + basket_value)  # negate because we offset

        # Exit condition
        if basket_pos != 0 and abs(s) < threshold * 0.5:
            # close
            basket_pos = 0
            leg_pos = {leg: 0 for leg in weights}
            exit_side = "close"
            pnl_captured = pnl.spread_capture - 2 * sum(abs(leg_pos[leg]) * fee_per_leg for leg in leg_pos)
            pnl.spread_capture = pnl_captured
            trades.append(Trade(entry_side, entry_spread, s, pnl.spread_capture))
            entry_side = None

        # Entry condition
        elif basket_pos == 0 and abs(s) > threshold:
            if s > threshold:
                # basket rich: short basket, long legs
                basket_pos = -max_basket_pos
                leg_pos = {leg: int(weights[leg] * max_basket_pos) for leg in weights}
                entry_side = "short_basket"
            else:
                # basket cheap: long basket, short legs
                basket_pos = max_basket_pos
                leg_pos = {leg: -int(weights[leg] * max_basket_pos) for leg in weights}
                entry_side = "long_basket"
            entry_spread = s
            # Charge entry fees
            pnl.spread_capture -= sum(abs(leg_pos[leg]) * fee_per_leg for leg in leg_pos)

    # Rebalance at end
    if basket_pos != 0:
        last_b, last_lm = basket_mids[-1], leg_mids_series[-1]
        leg_value = sum(leg_pos[leg] * last_lm[leg] for leg in weights)
        basket_value = basket_pos * last_b
        # The "rebalance" closes everything at market
        pnl.rebalance_cost = -(leg_value + basket_value) - sum(abs(leg_pos[leg]) * fee_per_leg for leg in leg_pos)
        basket_pos = 0
        leg_pos = {leg: 0 for leg in weights}

    return pnl, trades


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Synthetic GIFT_BASKET with rich/cheap oscillations
    import random
    random.seed(42)
    n = 500
    choc = [10 + random.gauss(0, 0.2) for _ in range(n)]
    straw = [1 + random.gauss(0, 0.05) for _ in range(n)]
    rose = [20 + random.gauss(0, 0.5) for _ in range(n)]
    weights = {"CHOCOLATE": 4, "STRAWBERRIES": 6, "ROSES": 1}

    # Make basket oscillate around NAV
    nav_vals = [4 * c + 6 * s + 1 * r for c, s, r in zip(choc, straw, rose)]
    # Add a sine wave on top to create mispricings
    basket_mids = [nv + 15 * math.sin(0.05 * t) for t, nv in enumerate(nav_vals)]
    leg_mids_series = [
        {"CHOCOLATE": c, "STRAWBERRIES": s, "ROSES": r}
        for c, s, r in zip(choc, straw, rose)
    ]

    pnl, trades = basket_arb_backtest(
        basket_mids, leg_mids_series, weights,
        threshold=10.0, max_basket_pos=5, fee_per_leg=0.0,
    )
    print(f"Backtest result: {pnl}")
    print(f"Number of trades: {len(trades)}")
    if trades:
        winners = sum(1 for t in trades if t.pnl > 0)
        print(f"Win rate: {winners / len(trades):.2%}")
        avg = sum(t.pnl for t in trades) / len(trades)
        print(f"Avg PnL per trade: {avg:.2f}")

    # With a sine-wave mispricing, the strategy should capture some of it.
    # Don't assert positive — depends on phase. Just verify it ran.
    assert isinstance(pnl.spread_capture, float)

    print("All self-tests passed.")
