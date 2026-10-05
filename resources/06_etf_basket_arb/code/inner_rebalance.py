"""
Module 06 — Inner rebalancing for PEBBLE-style constrained baskets.

Run the self-test:
    python inner_rebalance.py
"""

from __future__ import annotations
import math
from typing import Dict, List, Tuple


def inner_rebalance_signal(
    leg_mids: Dict[str, float],
    target_sum: float,
    weights_hint: Dict[str, float] = None,
) -> Dict[str, float]:
    """
    Compute fair prices for a constrained basket (sum to target_sum) and the
    mispricing for each leg. A leg is "rich" if its price is above fair, "cheap"
    if below.

    leg_mids: dict of leg -> mid price
    target_sum: the constraint (e.g., 50000 for PEBBLE)
    weights_hint: optional dict of leg -> fair weight (default: equal weight)

    Returns: dict of leg -> mispricing (positive = rich, negative = cheap)
    """
    legs = list(leg_mids.keys())
    n = len(legs)

    if weights_hint is None:
        # Default: equal weight
        weights = {leg: 1.0 / n for leg in legs}
    else:
        weights = weights_hint
        # Normalize
        total = sum(weights.values())
        weights = {leg: w / total for leg, w in weights.items()}

    # Fair price for each leg under the constraint
    fair_prices = {leg: target_sum * weights[leg] for leg in legs}

    # Mispricing: actual - fair
    mispricings = {leg: leg_mids[leg] - fair_prices[leg] for leg in legs}
    return mispricings


def inner_rebalance_trades(
    leg_mids: Dict[str, float],
    target_sum: float,
    threshold: float = 50.0,
    weights_hint: Dict[str, float] = None,
) -> Dict[str, Tuple[str, float]]:
    """
    Generate inner-rebalance trades. For each leg whose mispricing exceeds the
    threshold, sell it (if rich) or buy it (if cheap).

    Returns: dict of leg -> (side, qty_cash) where qty_cash is the dollar amount.
    """
    mispricings = inner_rebalance_signal(leg_mids, target_sum, weights_hint)
    trades = {}
    for leg, misp in mispricings.items():
        if abs(misp) < threshold:
            continue
        if misp > 0:
            trades[leg] = ("sell", abs(misp))
        else:
            trades[leg] = ("buy", abs(misp))
    return trades


def simulate_inner_rebalance(
    leg_mids_series: List[Dict[str, float]],
    target_sum: float,
    threshold: float = 50.0,
    weights_hint: Dict[str, float] = None,
) -> List[Tuple[int, Dict[str, Tuple[str, float]]]]:
    """
    Run inner-rebalance over a series. Returns a list of (tick, trades) tuples.
    """
    out = []
    for t, lm in enumerate(leg_mids_series):
        trades = inner_rebalance_trades(lm, target_sum, threshold, weights_hint)
        if trades:
            out.append((t, trades))
    return out


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # PEBBLE-style: 5 assets summing to 50,000; one is rich, one is cheap
    leg_mids = {"A": 10500, "B": 9800, "C": 10000, "D": 9900, "E": 10000}
    # Fair: 10,000 each
    misp = inner_rebalance_signal(leg_mids, target_sum=50000)
    print(f"Mispricings: {misp}")
    assert abs(misp["A"] - 500) < 1e-9
    assert abs(misp["B"] - (-200)) < 1e-9
    assert abs(misp["C"]) < 1e-9
    assert abs(misp["D"] - (-100)) < 1e-9
    assert abs(misp["E"]) < 1e-9

    # Trades
    trades = inner_rebalance_trades(leg_mids, target_sum=50000, threshold=100)
    print(f"Trades: {trades}")
    assert trades == {"A": ("sell", 500), "B": ("buy", 200), "D": ("buy", 100)}

    # With weights hint
    weights = {"A": 0.30, "B": 0.20, "C": 0.20, "D": 0.15, "E": 0.15}
    misp_w = inner_rebalance_signal(leg_mids, target_sum=50000, weights_hint=weights)
    print(f"Mispricings with weights: {misp_w}")
    # Fair prices: A=15000, B=10000, C=10000, D=7500, E=7500
    assert abs(misp_w["A"] - (10500 - 15000)) < 1e-9
    assert abs(misp_w["B"] - (9800 - 10000)) < 1e-9
    assert abs(misp_w["C"]) < 1e-9
    assert abs(misp_w["D"] - (9900 - 7500)) < 1e-9
    assert abs(misp_w["E"] - (10000 - 7500)) < 1e-9

    # Simulate
    series = [leg_mids, leg_mids, leg_mids]  # same mid
    sim = simulate_inner_rebalance(series, target_sum=50000, threshold=100)
    print(f"Simulate result: {sim}")
    assert len(sim) == 3  # trades fire every tick in this synthetic

    # No trade below threshold
    small = {"A": 10010, "B": 10000, "C": 10000, "D": 9990, "E": 10000}
    no_trade = inner_rebalance_trades(small, target_sum=50000, threshold=100)
    assert no_trade == {}

    print("All self-tests passed.")
