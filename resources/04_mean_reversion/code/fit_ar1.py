"""
Module 04 — Fit AR(1) and OU on a price series.

Run the self-test (synthetic data):
    python fit_ar1.py
"""

from __future__ import annotations
import math
import numpy as np
from typing import Dict, Any


def fit_ar1(prices) -> Dict[str, Any]:
    """
    Fit AR(1) to a price series.

    prices: list or array of prices (oldest first, most recent last)
    Returns: dict with c, beta, sigma_eps, mu, sigma_p, half_life
    """
    p = np.asarray(prices, dtype=float)
    if len(p) < 3:
        return {"c": 0, "beta": 0, "sigma_eps": 0, "mu": p.mean() if len(p) else 0,
                "sigma_p": 0, "half_life": float("inf")}

    # Use statsmodels if available, else fall back to closed-form OLS
    try:
        from statsmodels.tsa.ar_model import AutoReg
        model = AutoReg(p, lags=1).fit()
        c = float(model.params[0])
        beta = float(model.params[1])
        sigma_eps = float(np.sqrt(model.sigma2))
    except Exception:
        # Closed-form OLS for AR(1): beta = Cov(p_t, p_{t-1}) / Var(p_{t-1})
        p_lag = p[:-1]
        p_cur = p[1:]
        beta = float(np.cov(p_lag, p_cur, ddof=0)[0, 1] / np.var(p_lag, ddof=0)) if np.var(p_lag) > 0 else 0
        c = float(p_cur.mean() - beta * p_lag.mean())
        residuals = p_cur - (c + beta * p_lag)
        sigma_eps = float(np.std(residuals, ddof=1))

    if abs(1 - beta) > 1e-9:
        mu = c / (1 - beta)
    else:
        mu = float(p.mean())
    if abs(beta) < 1:
        sigma_p = sigma_eps / math.sqrt(1 - beta ** 2)
    else:
        sigma_p = float("inf")
    if 0 < beta < 1:
        half_life = -math.log(2) / math.log(beta)
    else:
        half_life = float("inf")

    return {
        "c": c, "beta": beta, "sigma_eps": sigma_eps,
        "mu": mu, "sigma_p": sigma_p, "half_life": half_life
    }


def fit_ou(prices, dt: float = 1.0) -> Dict[str, Any]:
    """
    Fit OU process by OLS on the discretized form.
    dp = a + b * p  =>  b = -theta * dt.
    """
    p = np.asarray(prices, dtype=float)
    if len(p) < 3:
        return {"theta": 0, "mu": float(p.mean()) if len(p) else 0,
                "sigma": 0, "half_life": float("inf")}
    dp = np.diff(p)
    p_lag = p[:-1]
    # Linear regression: dp = a + b * p_lag
    A = np.vstack([p_lag, np.ones_like(p_lag)]).T
    result = np.linalg.lstsq(A, dp, rcond=None)
    b, a = result[0]
    theta = -b / dt if dt > 0 else 0
    mu = a / (theta * dt) if abs(theta) > 1e-12 else float(p.mean())
    residuals = dp - (a + b * p_lag)
    sigma = float(np.std(residuals, ddof=1) / math.sqrt(dt))
    half_life = math.log(2) / theta if theta > 0 else float("inf")
    return {"theta": float(theta), "mu": mu, "sigma": sigma, "half_life": half_life}


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Synthetic AR(1) series: c=2, beta=0.9, sigma_eps=1
    # Long-term mean mu = 2 / (1 - 0.9) = 20
    np.random.seed(42)
    n = 1000
    prices = [10.0]
    c_true, beta_true, sigma_true = 2.0, 0.9, 1.0
    for _ in range(n - 1):
        prices.append(c_true + beta_true * prices[-1] + np.random.normal(0, sigma_true))

    p = fit_ar1(prices)
    print(f"AR(1) fit on synthetic data:")
    for k, v in p.items():
        print(f"  {k:12s} = {v:.4f}" if isinstance(v, float) else f"  {k:12s} = {v}")

    assert abs(p["c"] - c_true) < 0.5, f"c estimate {p['c']} too far from {c_true}"
    assert abs(p["beta"] - beta_true) < 0.05, f"beta {p['beta']} too far from {beta_true}"
    assert abs(p["mu"] - 20.0) < 5.0, f"mu {p['mu']} too far from 20"
    # True half-life for beta=0.9 is -log(2)/log(0.9) = 6.58; fitted should be in [5, 10]
    assert 5 < p["half_life"] < 10, f"half-life {p['half_life']} out of range"

    # OU fit on the same data
    o = fit_ou(prices, dt=1.0)
    print(f"OU fit:")
    for k, v in o.items():
        print(f"  {k:12s} = {v:.4f}" if isinstance(v, float) else f"  {k:12s} = {v}")
    assert o["theta"] > 0, f"theta should be positive, got {o['theta']}"
    assert 5 < o["half_life"] < 10, f"OU half-life {o['half_life']} out of range"

    # Edge: short series — should not raise
    short = fit_ar1([10, 11, 12])
    assert "c" in short and "beta" in short  # function returns the dict, even for short series

    print("All self-tests passed.")
