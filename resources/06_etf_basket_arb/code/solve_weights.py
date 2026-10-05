"""
Module 06 — Solve for basket weights via OLS.

Run the self-test (synthetic GIFT_BASKET-like data):
    python solve_weights.py
"""

from __future__ import annotations
import numpy as np
from typing import Dict, List, Tuple


def solve_weights(basket_prices: List[float], leg_prices: List[List[float]]) -> Tuple[List[float], float]:
    """
    Recover basket weights from data via OLS.

    basket_prices: list of historical basket mid prices, length T
    leg_prices: list of lists, T x K — each row is the K leg mids at that tick

    Returns: (weights, intercept)
        weights: list of length K
        intercept: scalar (usually 0 for a well-formed basket)
    """
    X = np.asarray(leg_prices, dtype=float)  # T x K
    y = np.asarray(basket_prices, dtype=float)
    if X.shape[0] != y.shape[0]:
        raise ValueError(f"Length mismatch: basket has {y.shape[0]} rows, legs have {X.shape[0]}")
    if X.shape[0] < X.shape[1] + 1:
        raise ValueError(f"Need at least {X.shape[1] + 1} observations; got {X.shape[0]}")

    # Add intercept column
    A = np.column_stack([np.ones(X.shape[0]), X])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    intercept = float(coef[0])
    weights = [float(c) for c in coef[1:]]
    return weights, intercept


def round_to_integers(weights: List[float], max_dev: float = 0.1) -> List[int]:
    """Round weights to integers if they're close. Returns the integer weights."""
    rounded = []
    for w in weights:
        r = round(w)
        if abs(w - r) > max_dev:
            # too far from integer; keep as float
            rounded.append(int(round(w)))
        else:
            rounded.append(int(r))
    return rounded


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Synthetic GIFT_BASKET-like: 4, 6, 1 with noise
    np.random.seed(42)
    n = 1000
    true_weights = [4.0, 6.0, 1.0]
    leg_mids = [
        np.random.uniform(8, 12, n),    # chocolate
        np.random.uniform(0.5, 1.5, n), # strawberry
        np.random.uniform(18, 22, n),   # rose
    ]
    leg_prices = list(zip(*leg_mids))  # T x K
    basket_clean = [sum(w * p for w, p in zip(true_weights, row)) for row in leg_prices]
    basket_prices = [b + np.random.normal(0, 0.5) for b in basket_clean]

    weights, intercept = solve_weights(basket_prices, leg_prices)
    print(f"Recovered weights: {weights}")
    print(f"True weights:     {true_weights}")
    print(f"Intercept:        {intercept:.4f}")
    assert abs(weights[0] - 4.0) < 0.1
    assert abs(weights[1] - 6.0) < 0.1
    assert abs(weights[2] - 1.0) < 0.1
    assert abs(intercept) < 0.5, f"Intercept {intercept} should be ~0"

    # Round to integers
    int_weights = round_to_integers(weights)
    print(f"Integer weights:  {int_weights}")
    assert int_weights == [4, 6, 1]

    # Noisy / non-integer weights
    noisy_weights = [3.95, 6.04, 1.02]
    assert round_to_integers(noisy_weights) == [4, 6, 1]

    # Edge: too few observations
    try:
        solve_weights([100, 101], [[1, 2], [3, 4]])
        assert False, "Should have raised"
    except ValueError:
        pass

    print("All self-tests passed.")
