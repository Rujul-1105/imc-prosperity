"""
Module 16 — Full grid-jump backtester.

Run the self-test (synthetic GBM-on-grid data):
    python grid_strategy.py
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from smooth import ema_smoother
from jump_signal import grid_jump_signal, next_grid


@dataclass
class PnLAttribution:
    grid_jump_alpha: float = 0.0
    inventory_drift: float = 0.0
    rebalance_cost: float = 0.0

    @property
    def total(self) -> float:
        return self.grid_jump_alpha + self.inventory_drift + self.rebalance_cost

    def __repr__(self):
        return (f"PnL(grid={self.grid_jump_alpha:.2f}, "
                f"drift={self.inventory_drift:.2f}, "
                f"rebalance={self.rebalance_cost:.2f}, "
                f"total={self.total:.2f})")


def simulate_gbm_on_grid(
    s0: float, sigma: float, n_ticks: int, dt: float = 1.0, mu: float = 0.0,
    grid_size: float = 1.0, seed: int = 42,
) -> Tuple[List[float], List[float]]:
    """
    Simulate a GBM and project onto a grid.
    Returns: (true_prices, displays)
    """
    import numpy as np
    rng = np.random.default_rng(seed)
    true = [s0]
    for _ in range(n_ticks - 1):
        eps = rng.normal()
        s_new = true[-1] * math.exp((mu - 0.5 * sigma ** 2) * dt + sigma * math.sqrt(dt) * eps)
        true.append(s_new)
    displays = [round(s / grid_size) * grid_size for s in true]
    return true, displays


def backtest_grid_jump(
    displays: List[float],
    grid_size: float = 1.0,
    alpha: float = 0.1,
    fee: float = 0.0,
) -> PnLAttribution:
    """
    Backtest the grid-jump strategy on a display series.
    Naive fill model: we trade at the next display, with fee applied each side.
    """
    pnl = PnLAttribution()
    smoothed = ema_smoother(displays, alpha=alpha)
    inventory = 0
    entry_price = 0.0

    for t in range(len(displays) - 1):
        signal = grid_jump_signal(displays[t], smoothed[t], grid_size=grid_size)
        next_display = displays[t + 1]

        if signal == "buy" and inventory <= 0:
            # Enter long: buy at displays[t] (current), sell at next_display
            inventory = 1
            entry_price = displays[t]
            # The "grid jump alpha" is realized when next_display happens
            pnl.grid_jump_alpha += (next_display - entry_price) - 2 * fee
            inventory = 0   # we close immediately on the next tick
        elif signal == "sell" and inventory >= 0:
            # Enter short: sell at displays[t], cover at next_display
            inventory = -1
            entry_price = displays[t]
            pnl.grid_jump_alpha += (entry_price - next_display) - 2 * fee
            inventory = 0
        # Inventory drift: in this model, we always flatten on next tick, so no drift

    return pnl


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Generate synthetic GBM-on-grid
    true, displays = simulate_gbm_on_grid(
        s0=100.0, sigma=0.05, n_ticks=2000, dt=1.0, mu=0.0, grid_size=1.0, seed=42
    )
    print(f"Generated {len(displays)} ticks. First 10 displays: {displays[:10]}")

    # Run backtest
    pnl = backtest_grid_jump(displays, grid_size=1.0, alpha=0.1, fee=0.0)
    print(f"Backtest (α=0.1, fee=0): {pnl}")

    # With small fees
    pnl_fee = backtest_grid_jump(displays, grid_size=1.0, alpha=0.1, fee=0.1)
    print(f"Backtest (α=0.1, fee=0.1): {pnl_fee}")
    assert pnl_fee.total < pnl.total, "Adding fees should reduce PnL"

    # Alpha sweep
    print("\nAlpha sweep:")
    for a in [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7]:
        p = backtest_grid_jump(displays, grid_size=1.0, alpha=a, fee=0.0)
        print(f"  α={a:5.2f}: {p}")

    # Verify alpha matters
    p_a_low = backtest_grid_jump(displays, grid_size=1.0, alpha=0.02, fee=0.0)
    p_a_high = backtest_grid_jump(displays, grid_size=1.0, alpha=0.7, fee=0.0)
    assert p_a_low.grid_jump_alpha != p_a_high.grid_jump_alpha, "Alpha should affect PnL"

    print("All self-tests passed.")
