"""
Module 03 — Avellaneda-Stoikov (2008) standalone implementation.
Re-derived from arXiv:1708.04928.

Run the self-test:
    python avellaneda_stoikov.py
"""

from __future__ import annotations
import math
from typing import Optional, Tuple


def as_quotes(
    mid: float,
    inventory: int,
    sigma: float,
    tau: float,
    gamma: float,
    kappa: float,
    max_pos: int = 20,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Avellaneda-Stoikov (2008) market-making quotes.

    mid:       current mid (or microprice) of the asset
    inventory: signed inventory (positive = long)
    sigma:     per-unit-time volatility
    tau:       T - t, time to terminal (same units as 1/sigma^2)
    gamma:     risk aversion parameter
    kappa:     order arrival rate (per unit time)
    max_pos:   hard inventory cap

    Returns: (bid, ask) honoring max_pos.
    """
    if sigma <= 0 or tau <= 0 or gamma <= 0 or kappa <= 0:
        return None, None

    sigma2 = sigma ** 2
    reservation = mid - inventory * gamma * sigma2 * tau
    half_spread = (gamma * sigma2 * tau) / 2 + (2 / gamma) * math.log(1 + gamma / kappa)
    bid = reservation - half_spread
    ask = reservation + half_spread

    if inventory >= max_pos:
        bid = None
    if inventory <= -max_pos:
        ask = None

    return bid, ask


def estimate_sigma(prices, lookback: int = 50) -> float:
    """Rolling realized vol from a list of mid prices. Returns per-step std."""
    if len(prices) < 2:
        return 0.0
    window = prices[-(lookback + 1):]
    deltas = [window[i] - window[i - 1] for i in range(1, len(window))]
    if not deltas:
        return 0.0
    mean = sum(deltas) / len(deltas)
    var = sum((d - mean) ** 2 for d in deltas) / max(1, len(deltas) - 1)
    return math.sqrt(var)


def estimate_kappa(fill_events: int, time_units: float) -> float:
    """
    Estimate order arrival rate from historical fills.
    fill_events: total number of touch fills observed
    time_units: total time observed (same units as tau)
    """
    if time_units <= 0:
        return 0.0
    return fill_events / time_units


def tune_gamma(prices, inventory_pnl, gamma_grid=None):
    """
    Pick gamma with highest Sharpe from a grid.
    prices: list of mid prices
    inventory_pnl: list of inventory-weighted prices (your exposure over time)

    NOTE: this is a placeholder; in practice you run a full backtest per gamma.
    The real version lives in 03_market_making/code/backtest_mm.py.
    """
    if gamma_grid is None:
        gamma_grid = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
    return gamma_grid  # placeholder; the backtester does the real work


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Zero inventory, low vol, near-end: tight quotes around mid
    bid, ask = as_quotes(mid=100, inventory=0, sigma=0.5, tau=10, gamma=0.1, kappa=1.5)
    print(f"AS (zero inv, low vol): bid={bid:.4f}, ask={ask:.4f}, spread={ask - bid:.4f}")
    assert bid is not None and ask is not None
    assert bid < 100 < ask

    # Long inventory: reservation below mid (encouraging sells)
    # Note: keep inventory < max_pos so the bid isn't hard-capped to None.
    bid_long, ask_long = as_quotes(mid=100, inventory=10, sigma=0.5, tau=10, gamma=0.1, kappa=1.5, max_pos=20)
    print(f"AS (long 10): bid={bid_long:.4f}, ask={ask_long:.4f}, reservation={100 - 10*0.1*0.25*10:.4f}")
    # reservation = 100 - 10*0.1*0.25*10 = 100 - 2.5 = 97.5
    # half_spread = 0.1*0.25*10/2 + (2/0.1)*ln(1 + 0.1/1.5)
    #             = 0.125 + 20*ln(1.0667) ≈ 0.125 + 1.307 ≈ 1.432
    # bid = 97.5 - 1.432 = 96.068; ask = 97.5 + 1.432 = 98.932
    assert 95 < bid_long < 97
    assert 98 < ask_long < 99

    # Hard cap: at max_pos the bid is killed
    bid_cap, _ = as_quotes(mid=100, inventory=20, sigma=0.5, tau=10, gamma=0.1, kappa=1.5, max_pos=20)
    assert bid_cap is None
    print("Hard cap enforced.")

    # Sigma estimate
    import random
    random.seed(42)
    prices = [100.0]
    for _ in range(200):
        prices.append(prices[-1] + random.gauss(0, 0.5))
    sigma = estimate_sigma(prices, lookback=50)
    print(f"Estimated sigma: {sigma:.4f} (target 0.5)")
    assert 0.4 < sigma < 0.6

    print("All self-tests passed.")
