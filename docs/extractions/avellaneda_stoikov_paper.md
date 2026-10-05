# Extraction: Avellaneda & Stoikov (2008)

**Source**: Avellaneda & Stoikov, "High-frequency trading in a limit order book." arXiv:1708.04928.
**Used in**: Module 03 (Market making).

## The problem

A market-maker posts bid and ask quotes in a single stock. The mid-price follows arithmetic Brownian motion:

```
dS = σ dW
```

The market-maker's inventory `q` evolves based on fills. The goal: maximize expected utility of terminal PnL minus inventory variance.

## The solution

Two key equations:

### 1. Reservation price

The reservation price is the price at which the market-maker is indifferent between buying and not buying. It's the mid minus an inventory penalty:

```
r(s, q, t) = s - q · γ · σ² · (T - t)
```

where:
- `s` = mid price
- `q` = current inventory (positive = long)
- `γ` = risk aversion parameter
- `σ` = volatility
- `T - t` = time to terminal

If you're long (q > 0), the reservation price is *below* the mid — you're willing to sell, less willing to buy. If you're short, the opposite.

### 2. Optimal spread

The optimal half-spread (distance from reservation to bid/ask):

```
δ(s, q, t) = (γ · σ² · (T - t)) / 2 + (2 / γ) · ln(1 + γ / κ)
```

where:
- `κ` = order arrival rate parameter (a measure of "how fast do orders arrive at the touch?")

The first term widens the spread with volatility and time. The second is a constant offset based on the order flow.

### 3. Final quotes

```
bid = r(s, q, t) - δ(s, q, t)
ask = r(s, q, t) + δ(s, q, t)
```

Substituting:

```
bid = s - q·γ·σ²·(T-t) - γ·σ²·(T-t)/2 - (2/γ)·ln(1 + γ/κ)
ask = s - q·γ·σ²·(T-t) + γ·σ²·(T-t)/2 + (2/γ)·ln(1 + γ/κ)
```

## How to estimate parameters

### γ (risk aversion)

Back out from historical inventory. The market-maker's inventory variance should equal `1/γ`. Estimate from your own backtest.

In practice, tune γ by sweeping over a grid and picking the value that gives the best risk-adjusted PnL.

### σ (volatility)

Use the rolling realized vol over the past N ticks. N=50 is a good default.

### κ (order arrival rate)

The number of orders per unit time arriving at the touch. Estimate from historical fill rate: `κ = (number of fills at touch) / (time at touch)`.

### T - t (time to terminal)

In a continuous-time model, this is the time horizon. In a tick-by-tick backtest, set `T - t = (num_ticks_remaining / num_ticks_total) × horizon_seconds`. The horizon is round-specific (P3 R1 was 1 hour per day; check the spec).

## Code skeleton (Python)

```python
import math

def as_quotes(s, q, sigma, tau, gamma, kappa):
    """
    s:     mid price
    q:     inventory (signed)
    sigma: volatility
    tau:   T - t, time to terminal (in same units as 1/sigma²)
    gamma: risk aversion
    kappa: order arrival rate
    """
    reservation = s - q * gamma * sigma**2 * tau
    half_spread = (gamma * sigma**2 * tau) / 2 + (2 / gamma) * math.log(1 + gamma / kappa)
    return reservation - half_spread, reservation + half_spread
```

## When AS loses to Wall-Mid

In P3 R1 (Timo's experiment), Wall-Mid beat AS on RAINFOREST_RESIN. Why?

- AS assumes mid is GBM. AMETHYSTS / RAINFOREST_RESIN has a known FV — GBM is wrong.
- AS doesn't see walls. Walls are predictable; AS treats them as noise.
- AS requires tuning γ and κ. Wall-Mid has no parameters.

Rule of thumb:
- **FFV rounds**: Wall-Mid or a modified AS with the FV as a price-level target.
- **GBM / mean-reverting**: AS is competitive.
- **Thin book / large ticks**: AS over-fits; simpler is better.

## How this maps to our modules

- **Module 03** (Market making): the entire mathematical core.
- **Module 18** (Stochastic control, advanced): the full HJB derivation and extensions.

## What we did NOT extract

- The full HJB derivation (advanced; see Cartea-Jaimungal-Penã or module 18).
- Multiple asset extensions (the team doesn't need them in P5).
- The market-impact-adjusted version (the team doesn't need it in P5).
- Adverse selection models (Glosten-Milgrom; module 17).

## Source

- Avellaneda, M., & Stoikov, S. (2008). High-frequency trading in a limit order book. Quantitative Finance, 8(3), 217-224.
- arXiv:1708.04928.
- Reference code: `astraflow/avellaneda-stoikov` on GitHub.
