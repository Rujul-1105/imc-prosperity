"""
Module 06 — NAV and spread computation.

Run the self-test:
    python nav.py
"""

from __future__ import annotations
import math
from typing import Dict, List


def nav(leg_mids: Dict[str, float], weights: Dict[str, float]) -> float:
    """Net Asset Value = sum(weight * mid) over all legs."""
    return sum(weights[leg] * leg_mids[leg] for leg in weights)


def spread(basket_mid: float, leg_mids: Dict[str, float], weights: Dict[str, float]) -> float:
    """basket_mid - NAV. Positive = basket rich; negative = basket cheap."""
    return basket_mid - nav(leg_mids, weights)


def spread_series(
    basket_mids: List[float],
    leg_mids_series: List[Dict[str, float]],
    weights: Dict[str, float],
) -> List[float]:
    """Compute the spread at every tick."""
    return [spread(b, lm, weights) for b, lm in zip(basket_mids, leg_mids_series)]


def spread_stats(spread_series: List[float]) -> Dict[str, float]:
    """Mean, std, and basic stats of a spread series."""
    n = len(spread_series)
    if n == 0:
        return {"mean": 0, "std": 0, "min": 0, "max": 0, "median": 0}
    mean = sum(spread_series) / n
    var = sum((x - mean) ** 2 for x in spread_series) / max(1, n - 1)
    std = math.sqrt(var)
    sorted_s = sorted(spread_series)
    median = sorted_s[n // 2] if n % 2 == 1 else (sorted_s[n // 2 - 1] + sorted_s[n // 2]) / 2
    return {
        "mean": mean, "std": std,
        "min": min(spread_series), "max": max(spread_series),
        "median": median
    }


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # GIFT_BASKET-style: 4 choc, 6 straw, 1 rose
    weights = {"CHOCOLATE": 4, "STRAWBERRIES": 6, "ROSES": 1}
    mids = {"CHOCOLATE": 10, "STRAWBERRIES": 1, "ROSES": 20}
    expected_nav = 4 * 10 + 6 * 1 + 1 * 20
    assert nav(mids, weights) == expected_nav

    # Spread
    basket_mid = 60
    assert spread(basket_mid, mids, weights) == basket_mid - expected_nav

    # Series
    series = spread_series(
        [60, 55, 50, 60],
        [
            {"CHOCOLATE": 10, "STRAWBERRIES": 1, "ROSES": 20},
            {"CHOCOLATE": 10, "STRAWBERRIES": 1, "ROSES": 20},
            {"CHOCOLATE": 9, "STRAWBERRIES": 1, "ROSES": 20},
            {"CHOCOLATE": 10, "STRAWBERRIES": 1, "ROSES": 20},
        ],
        weights,
    )
    print(f"Spread series: {series}")
    # NAV = 4*10 + 6*1 + 1*20 = 40 + 6 + 20 = 66
    # First: 60 - 66 = -6; Second: 55 - 66 = -11; Third: 50 - (4*9 + 6*1 + 1*20) = 50 - 62 = -12; Fourth: 60 - 66 = -6
    assert series == [-6, -11, -12, -6]

    # Stats
    stats = spread_stats(series)
    print(f"Spread stats: {stats}")
    assert stats["min"] == -12
    assert stats["max"] == -6
    assert abs(stats["mean"] - (-6 - 11 - 12 - 6) / 4) < 1e-9

    # Empty
    empty_stats = spread_stats([])
    assert empty_stats == {"mean": 0, "std": 0, "min": 0, "max": 0, "median": 0}

    print("All self-tests passed.")
