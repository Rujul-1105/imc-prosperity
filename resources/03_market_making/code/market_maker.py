"""
Module 03 — Market Making
A reusable market-making class with three quoting strategies: AS, Wall-Mid, hybrid.

Run the self-test:
    python market_maker.py
"""

from __future__ import annotations
import math
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass, field


@dataclass
class Quote:
    bid: Optional[float]
    ask: Optional[float]


@dataclass
class MarketState:
    """Minimum state needed by all three strategies."""
    mid: float
    bids: List[Tuple[float, float]] = field(default_factory=list)  # (price, volume), best first
    asks: List[Tuple[float, float]] = field(default_factory=list)
    inventory: int = 0
    sigma: float = 0.0    # per-tick volatility estimate
    tau: float = 60.0     # time to terminal (in same units as 1/sigma^2)
    gamma: float = 0.1    # risk aversion
    kappa: float = 1.5    # order arrival rate
    max_pos: int = 20     # hard inventory cap


class MarketMaker:
    """Three quoting strategies: AS, Wall-Mid, hybrid. Plus helpers."""

    # --------------------------------------------------------------------- AS
    def as_quotes(self, s: MarketState) -> Quote:
        """Avellaneda-Stoikov (2008). Returns (bid, ask)."""
        if s.sigma <= 0 or s.tau <= 0:
            return Quote(None, None)
        gamma, sigma2, tau = s.gamma, s.sigma ** 2, s.tau
        reservation = s.mid - s.inventory * gamma * sigma2 * tau
        half_spread = (gamma * sigma2 * tau) / 2 + (2 / gamma) * math.log(1 + gamma / s.kappa)
        return self._cap(reservation - half_spread, reservation + half_spread, s)

    # ------------------------------------------------------------------- Wall-Mid
    def wall_mid_quotes(self, s: MarketState, skew_per_unit: float = 0.2) -> Quote:
        """Timo Diehm's Wall-Mid heuristic. No math, just read the book."""
        if not s.bids or not s.asks:
            return Quote(None, None)
        bid_wall = sorted(s.bids, key=lambda x: -x[1])[0][0]
        ask_wall = sorted(s.asks, key=lambda x: -x[1])[0][0]
        skew = s.inventory * skew_per_unit
        return self._cap(bid_wall + 1 - skew, ask_wall - 1 - skew, s)

    # ------------------------------------------------------------------ Hybrid
    def hybrid_quotes(self, s: MarketState, skew_per_unit: float = 0.2) -> Quote:
        """Wall-Mid center + AS inventory skew. The best of both."""
        if not s.bids or not s.asks:
            return Quote(None, None)
        bid_wall = sorted(s.bids, key=lambda x: -x[1])[0][0]
        ask_wall = sorted(s.asks, key=lambda x: -x[1])[0][0]
        # AS inventory skew only
        as_skew = s.inventory * s.gamma * (s.sigma ** 2) * s.tau
        bid = bid_wall + 1 - as_skew
        ask = ask_wall - 1 - as_skew
        return self._cap(bid, ask, s)

    # ------------------------------------------------------------------ Helpers
    def _cap(self, bid: float, ask: float, s: MarketState) -> Quote:
        if s.inventory >= s.max_pos:
            bid = None
        if s.inventory <= -s.max_pos:
            ask = None
        if bid is not None and ask is not None and bid >= ask:
            # crossed; widen to a 1-tick minimum spread
            mid = (bid + ask) / 2
            bid, ask = mid - 0.5, mid + 0.5
        return Quote(bid=bid, ask=ask)

    @staticmethod
    def estimate_sigma(prices: List[float], lookback: int = 50) -> float:
        """Rolling realized vol over the past N prices. Returns per-step std."""
        if len(prices) < 2:
            return 0.0
        window = prices[-(lookback + 1):]
        deltas = [window[i] - window[i - 1] for i in range(1, len(window))]
        if not deltas:
            return 0.0
        mean = sum(deltas) / len(deltas)
        var = sum((d - mean) ** 2 for d in deltas) / max(1, len(deltas) - 1)
        return math.sqrt(var)


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    mm = MarketMaker()
    state = MarketState(
        mid=100.0,
        bids=[(99, 50), (98, 30), (97, 20)],
        asks=[(101, 5), (102, 40), (103, 10)],
        inventory=10,
        sigma=0.5,
        tau=60.0,
        gamma=0.1,
        kappa=1.5,
        max_pos=20,
    )

    print("AS quotes:", mm.as_quotes(state))
    print("Wall-Mid quotes:", mm.wall_mid_quotes(state))
    print("Hybrid quotes:", mm.hybrid_quotes(state))

    # Sigma estimation
    import random
    random.seed(42)
    prices = [100.0]
    for _ in range(200):
        prices.append(prices[-1] + random.gauss(0, 0.5))
    sigma = mm.estimate_sigma(prices, lookback=50)
    print(f"Estimated sigma: {sigma:.4f}  (expected ~0.5)")
    assert 0.4 < sigma < 0.6, f"sigma {sigma} out of range"

    # Hard cap
    state.inventory = 25  # over max_pos
    q = mm.as_quotes(state)
    print(f"Capped quotes (inv=25, max=20): {q}")
    assert q.bid is None

    # Crossed check
    state.inventory = 0
    state.sigma = 100.0  # huge vol
    q = mm.as_quotes(state)
    print(f"Widened quotes (huge vol): {q}")
    assert q.bid is not None and q.ask is not None
    assert q.ask > q.bid

    print("All self-tests passed.")
