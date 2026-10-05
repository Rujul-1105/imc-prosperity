"""
Module 04 — Half-life helpers.

Run the self-test:
    python half_life.py
"""

from __future__ import annotations
import math


def half_life_from_beta(beta: float) -> float:
    """Half-life in steps for an AR(1) with parameter beta. Inf if not in (0, 1)."""
    if not (0 < beta < 1):
        return float("inf")
    return -math.log(2) / math.log(beta)


def beta_from_half_life(half_life: float) -> float:
    """Inverse: beta from a target half-life."""
    if half_life <= 0:
        return 0.0
    return math.exp(-math.log(2) / half_life)


def half_life_from_theta(theta: float) -> float:
    """Half-life in time units for an OU process with mean-reversion speed theta."""
    if theta <= 0:
        return float("inf")
    return math.log(2) / theta


def zscore(price: float, mu: float, sigma_p: float) -> float:
    """Standard z-score. Returns 0 if sigma_p is 0."""
    if sigma_p == 0:
        return 0.0
    return (price - mu) / sigma_p


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    assert abs(half_life_from_beta(0.5) - 1.0) < 1e-9
    assert abs(half_life_from_beta(0.9) - 6.5788) < 0.01
    assert half_life_from_beta(0) == float("inf")
    assert half_life_from_beta(1) == float("inf")
    assert half_life_from_beta(1.5) == float("inf")
    assert half_life_from_beta(-0.5) == float("inf")

    # Round-trip
    for hl in [1, 5, 10, 50, 100]:
        b = beta_from_half_life(hl)
        hl_back = half_life_from_beta(b)
        assert abs(hl - hl_back) < 1e-6, f"round-trip failed for {hl}: {b}, {hl_back}"

    # z-score
    assert zscore(100, 100, 5) == 0
    assert zscore(110, 100, 5) == 2
    assert zscore(90, 100, 5) == -2
    assert zscore(100, 100, 0) == 0

    # OU half-life
    assert abs(half_life_from_theta(0.1) - 6.9315) < 0.01
    assert half_life_from_theta(0) == float("inf")
    assert half_life_from_theta(-0.1) == float("inf")

    print("All self-tests passed.")
