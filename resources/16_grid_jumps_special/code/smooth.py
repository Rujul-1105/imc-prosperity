"""
Module 16 — EMA smoother for grid-projected prices.

Run the self-test:
    python smooth.py
"""

from __future__ import annotations
from typing import List


def ema_smoother(displays: List[float], alpha: float = 0.1) -> List[float]:
    """
    Smooth a sequence of grid-projected display prices via EMA.
    Returns a list of smoothed estimates.
    """
    if not displays:
        return []
    smoothed = []
    s = displays[0]
    for d in displays:
        s = alpha * d + (1 - alpha) * s
        smoothed.append(s)
    return smoothed


def kalman_like_smoother(displays: List[float], process_var: float = 1.0, obs_var: float = 1.0) -> List[float]:
    """
    A simple Kalman-like smoother. Models the true price as a random walk
    and the display as the true price + observation noise (the grid quantization).

    process_var: variance of true-price random-walk increments
    obs_var:     variance of observation noise (grid quantization ~ g²/12)
    """
    if not displays:
        return []
    out = []
    x = displays[0]   # estimate
    p = obs_var        # estimate variance
    for d in displays:
        # predict
        p = p + process_var
        # update
        k = p / (p + obs_var)        # Kalman gain
        x = x + k * (d - x)
        p = (1 - k) * p
        out.append(x)
    return out


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Constant input: smoother should converge to the constant
    smoothed = ema_smoother([100.0] * 100, alpha=0.1)
    assert all(abs(s - 100.0) < 1e-9 for s in smoothed)

    # Step change: smoother should adapt but with lag
    smoothed = ema_smoother([100.0] * 50 + [101.0] * 50, alpha=0.1)
    # At t=99 (50 steps after the change), the smoother should be close to 101 but not exactly
    assert 100.5 < smoothed[99] < 101.0, f"smoothed[99] = {smoothed[99]}"
    # At t=49 (right at the change), still 100
    assert smoothed[49] == 100.0

    # Empty
    assert ema_smoother([]) == []

    # Kalman
    ksmoothed = kalman_like_smoother([100.0] * 100, process_var=0.01, obs_var=0.1)
    assert all(abs(s - 100.0) < 0.5 for s in ksmoothed)

    ksmoothed = kalman_like_smoother([100.0] * 50 + [101.0] * 50, process_var=0.01, obs_var=0.1)
    # Should adapt, with some lag
    assert 100.5 < ksmoothed[99] < 101.5

    print("All self-tests passed.")
